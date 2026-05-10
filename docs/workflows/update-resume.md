# Update Resume Workflow

Use this when updating the current resume for a new target role, new job, new project, or refreshed positioning.

1. Identify the target role family and desired emphasis.
2. Check whether market/ATS guidance is fresh for that target.
3. Read `context/index.md` and the generated index most relevant to the target.
4. Use only context marked `resume_safe: true` and `approved_for_resume: true`, unless the candidate explicitly approves a new claim.
5. Edit `resumes/current/Jordan_Example_Resume.md`.
6. Keep the resume one page unless the candidate approves otherwise.
7. Translate internal project names into externally understandable descriptions.
8. Run `tools/check.sh`.
9. Inspect `resumes/current/preview.png`.
10. If creating a snapshot, archive it under `resumes/archive/YYYY-MM-DD-target-role-slug/` with `metadata.yaml`.

## Final Candidate

Do not run the full final review gate for every draft. When the candidate says the resume is final, ready to send, ready to apply, or asks for final review, follow `docs/workflows/final-resume-review.md`.

If the resume appears near-final but the candidate has not explicitly asked for final review, ask whether to run the final review gate before sending or applying.
