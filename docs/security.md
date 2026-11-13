# Security

This project's threat model and security setup. The rules are in the
standard's `security.md`; this file records what applies here. Review it at
the end of each phase, and when a change adds a component or a new way in.

## Threat model (lite)

**1. What are we building?** A local, offline CLI/library that reads image
and PDF files I give it and writes per-page OCR text to a JSON or CSV file.
No network calls and no secrets since S1.1.2 (Baidu removed). See
`architecture.md` → System context.

**2. What can go wrong?**

| Asset (worth protecting) | Entry point (how it could be reached) | What could go wrong | Likelihood | Impact |
|---|---|---|---|---|
| My documents' text (personal data) | Logs and output files | Document text ends up in logs or somewhere unexpected | Low | Med |
| The run itself | An input image or PDF, given directly or found in a folder I pass (corrupt or malicious) | A bad file crashes the whole run, or exploits a bug in Pillow / PyMuPDF | Med | Med |
| My machine | Dependencies (Pillow, PyMuPDF) | A vulnerable or look-alike package runs code with my permissions | Low | High |

**3. What are we doing about it?**
- Document text: never logged above DEBUG (NFR5); output goes only to the
  path I choose.
- Bad input file: folders expand to top-level image/PDF files only — no
  recursion, other files skipped (S1.1.4); skip-and-report — the file
  becomes an error in its page result and the run continues (NFR4,
  S1.1.5); file types checked by extension before opening (`io.py`); keep
  Pillow / PyMuPDF up to date.
- Dependencies: only well-known packages from PyPI, checked before adding
  (the standard's `security.md` → Dependencies); dependency audit each
  phase end (NFR2).

**4. Did it work?** Checked at the end of Phase 1 (2026-10-11): bad-file
handling tested through `run_pipeline()` and the CLI; a test confirms
document text is never logged above DEBUG; `pip-audit` clean (after
upgrading the venv's pip, PYSEC-2026-3721). Threat model still accurate: no
new entry points beyond folder input (S1.1.4). Dependabot alerts are off and
secret-scanning alerts weren't readable with the current `gh` login — check
on GitHub.

## Personal data

The text of my own documents passes through the pipeline. It's never
logged above DEBUG and is written only to the output file I choose. Sample
documents in `samples/` are generated and hold no real personal data.

## GitHub setup (GitHub only)

Turning these on is the user's call. Record what's on:

- [ ] Dependabot alerts (off, as of 2026-10-11)
- [ ] Dependabot security updates
- [ ] Secret scanning and push protection (not checked: not readable with the current `gh` login)
- [ ] `main` protected (PR required, no force pushes)
