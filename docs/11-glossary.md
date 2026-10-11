# Glossary

Project-specific terms, so you, the docs, the code, and AI agents all use
the same word for the same thing. One concept = one term — this is what
keeps names consistent across the codebase (see the naming rules in
`06-coding-conventions.md`).

- Add a term when a new concept appears, in the same change that
  introduces it.
- **Use instead of** lists the synonyms you've ruled out — if one of them
  shows up in code or docs, rename it.
- Keep the table sorted alphabetically.

| Term | Meaning | Use instead of |
|---|---|---|
| backend | An OCR engine behind the common interface: takes one page image, returns its lines of text with confidence. | "engine" (in code), "provider", "OCR service" |
| backend registry | The name → backend lookup used by `get_backend()`; adding a backend means registering it here. | "factory", "plugin list" |
| confidence | The backend's score (0–1) for how sure it is of a line's text. In CSV, the mean over a page's lines. | "score", "probability" |
| known text | The text a sample document really contains, saved next to it as `.txt`, used to judge OCR output. | "ground truth", "expected text", "answer key" |
| line | One line of recognized text on a page, with its confidence. | "result", "item", "block" |
| page | One image sent to OCR: an image file, or one rasterized page of a PDF. Numbered from 1. | "frame", "sheet" |
| page result | The `PageResult` for one page: source file, page number, text, lines, and error (if it failed). A file that fails to load gets one page result with no page number. | "result dict", "record", "output" |
| run | One call of `run_pipeline()` (or the CLI / UI) over a set of input files and folders. | "job", "batch", "session" |
| sample document | A generated file in `samples/` with no real personal data, used to test and judge OCR. | "fixture", "test doc" |
| skip-and-report | When a file or page fails, record the error in its page result, log a warning, and keep going. | "fail-soft", "continue on error" |
| source file | The input file a page came from (image or PDF), as given by the user or found in a folder. | "input path", "origin" |
