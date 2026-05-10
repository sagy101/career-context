# Ingest Career Context Workflow

Use this when adding new jobs, projects, awards, talks, or source materials.

1. Summarize the source at career-context level.
2. Do not copy proprietary source text, code, diagrams, endpoints, customer data, or credentials.
3. Create or update the right context file under `context/`.
4. Fill all required frontmatter fields.
5. Add `Resume Bullet Bank`, `Claims Needing Confirmation`, and `Do Not Include`.
6. Put local paths and internal links only in `Source Notes`.
7. Run `tools/build_context_indexes.py`.
8. Run `tools/validate_context.py`.
9. Append a short entry to `context/log.md`.
