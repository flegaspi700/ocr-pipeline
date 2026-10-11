# OCR Pipeline Review Notes

## Summary
This repository was scaffolded with a Python OCR pipeline package structure and a pluggable backend design. The project now includes:

- `pyproject.toml`
- `src/ocr_pipeline/` package modules
- `tests/` with unit tests for I/O, preprocessing, export, and backend logic
- `.github/workflows/python.yml` CI workflow
- `spec-kit.md` implementation and best-practice guide
- `review_notes.md` this file

## Current status
- **Update 2026-10-10 (S4.1.1):** the SSL error below no longer reproduces.
  A fresh `.venv` installs cleanly and all 8 tests pass. Setup notes are in
  `docs/03-tech-stack.md`. The rest of this file is the original review,
  kept for history.
- Code scaffold and repository structure are complete.
- A dedicated new virtual environment was created at `.venv2/`.
- Dependency installation failed due to SSL issues when connecting to PyPI.

## Root cause of installation failure
- `pip` could not download packages from `files.pythonhosted.org`. 
- The error was `SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1035)')`.
- This is an environment/network issue, not a code problem.

## Files to review
- `pyproject.toml`
- `README.md`
- `spec-kit.md`
- `src/ocr_pipeline/cli.py`
- `src/ocr_pipeline/io.py`
- `src/ocr_pipeline/preprocess.py`
- `src/ocr_pipeline/backend.py`
- `src/ocr_pipeline/export.py`
- `tests/test_io_and_preprocess.py`
- `tests/test_export.py`
- `tests/test_backend.py`
- `.github/workflows/python.yml`

## Next actions
1. Fix the environment/network issue so dependencies can be installed.
2. Run `pytest` once dependencies are available.
3. Confirm the CLI works with sample input and returns JSON/CSV output.
4. Add actual Baidu Unlimited-OCR credentials and verify the backend API integration.

## Notes for push
- `.venv/`, `.venv2/`, and `.vscode/` are intentionally ignored in `.gitignore`.
- Only source, docs, tests, and workflow files should be committed.
