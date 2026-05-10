# Market Scans

Market scans are dated snapshots of recruiter language, ATS keywords, role expectations, and resume implications for a target role family.

Create a new scan instead of overwriting an old one:

```text
guidance/market-scans/YYYY-MM-DD-target-role-slug.md
```

## Freshness Rules

During final resume review, refresh or create a scan automatically when:

- no scan exists for the target role family
- the latest AI / agentic / ML infrastructure scan is older than 45 days
- the latest general full-stack / platform scan is older than 90 days
- the latest resume-format / ATS fundamentals scan is older than 180 days
- the target role family, seniority, geography, company, or job description changed
- the user provides a specific job posting

## Trusted Sources

Prefer:

- official job postings from target companies
- reputable university career guidance
- official technology documentation
- official prompt-engineering docs when reviewing prompt quality
- NIST AI RMF/AIRC guidance when reviewing AI safety and trustworthiness language

Avoid generic resume blogs unless no better source exists. Mark generic sources as lower confidence.

## Required Sections

Each scan should include:

- target role family, seniority, geography, and date
- sources with URLs and access dates
- recurring recruiter keywords
- required vs nice-to-have skills
- seniority and leadership signals
- resume implications
- outdated or low-value terms to avoid
- changes since the previous scan, if one exists

## Machine-Readable Metadata

Every dated scan must include YAML frontmatter so agents and validators can enforce freshness:

```yaml
---
type: market-scan
scan_date: YYYY-MM-DD
target_role_family:
  - AI Engineer
seniority:
  - Senior
geography:
  - United States
max_age_days: 45
previous_scan:
changes_since_previous: Initial scan.
---
```

Run `tools/validate_market_scans.py` after adding or updating a scan.
