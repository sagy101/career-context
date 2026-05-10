# Career Context

Career Context is a durable, agent-friendly workspace for turning career evidence into sharp, targeted resumes.

Most resume updates start from scattered memory: old bullets, stale PDFs, half-remembered metrics, private project details, and a vague sense of what recruiters want now. This repo treats the resume as an evolving product instead. It keeps the source material, market guidance, review prompts, generated artifacts, and safety rules in one maintained system, so each future update starts from evidence instead of guesswork.

Use it to preserve the story behind the resume: what was built, what was measured, what can be said publicly, what should stay private, and why a particular version was positioned the way it was.

## What It Does

- Keeps the canonical resume in Markdown and regenerates DOCX, PDF, and preview artifacts.
- Organizes career context by company, role, project, skill, date, and target role.
- Separates confirmed outcomes, estimates, targets, and private source notes.
- Stores market scans and ATS guidance so positioning can evolve with the job market.
- Provides review prompts for recruiter fit, technical credibility, evidence quality, confidentiality, readability, leadership signal, and rendering.
- Preserves archived resume versions with metadata, notes, and extracted text.

## Why It Exists

A strong resume is not just writing. It is source control for professional evidence.

Career Context helps answer the questions that usually slow down a high-stakes resume update:

- Which claims are actually supported?
- Which details are public-safe?
- Which projects best match this target role?
- Which wording changed, and why?
- Which skills, systems, and outcomes should be emphasized now?
- Can the final DOCX/PDF be regenerated and reviewed consistently?

The goal is simple: make every future resume update faster, safer, better sourced, and more recruiter-ready than the last.

## Repository Map

```text
.
├── context/                 # Structured career evidence and generated indexes
├── resumes/current/         # Canonical Markdown plus generated DOCX/PDF/preview
├── resumes/archive/         # Versioned resume snapshots and notes
├── guidance/                # Market scans, ATS guidance, and public-safety rules
├── reviews/                 # Final-review prompts and reviewer guidance
├── docs/workflows/          # Repeatable workflows for updates and reviews
├── config/                  # Validation and rendering configuration
└── tools/                   # Build, render, inspect, and validation scripts
```

## Normal Update Flow

1. Read `AGENTS.md`.
2. Read `docs/workflows/update-resume.md`.
3. Identify the target role family, seniority, geography, and any specific job posting.
4. Refresh market guidance when positioning, skills, or ATS language may have changed.
5. Pull resume-safe evidence from `context/index.md` and generated context indexes.
6. Edit `resumes/current/Jordan_Example_Resume.md`.
7. Run `tools/check.sh`.
8. Inspect `resumes/current/preview.png`.

The canonical resume source is `resumes/current/Jordan_Example_Resume.md`. DOCX, PDF, and preview PNG files are generated artifacts.

Renderer layout defaults live in `config/resume-style.yaml`, so formatting can be tuned without rewriting the renderer.

## Local Setup

Install system render/check dependencies first:

```bash
# macOS
brew install --cask libreoffice
brew install poppler ripgrep

# Ubuntu
sudo apt-get update
sudo apt-get install -y libreoffice poppler-utils ripgrep fonts-crosextra-carlito fonts-liberation
```

Then install Python dependencies and run the preflight checks:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
tools/doctor.sh
PYTHON=.venv/bin/python tools/check.sh
```

## Safety Model

This workspace is designed for public-safe career context, not private employer archiving.

Do not commit proprietary source code, copied internal documents, credentials, customer data, confidential diagrams, endpoints, detailed implementation secrets, or private system records. Store structured, resume-safe summaries instead, and keep public claims tied to evidence and explicit boundaries.

Final resume artifacts should be boringly safe: no internal URLs, local source paths, customer-sensitive material, copied private text, or secret-like values.

## License

MIT. See `LICENSE`.
