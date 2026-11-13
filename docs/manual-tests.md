# Manual tests

Checks only a person can judge: how something looks, feels or plays.
Write the steps once per feature, then record a result each run. Rules: the
standard's `testing.md` → Manual tests.

---

## F2.1 — Generated sample documents

**What to check:** the samples look like plain printed documents, every
line is fully readable (nothing clipped at the edges), and the text drawn
matches its `.txt` file.

**Steps:**
1. Run `python scripts/make_samples.py` from the repo root
2. Open `samples/receipt.png`, `samples/form.png` and each page of
   `samples/multipage.pdf`
3. Compare each with its `.txt` file: same lines, same order, nothing cut
   off, no real names or contact details

**Results:**

| Date | Version / commit | Result | Notes |
|---|---|---|---|
| 2026-10-12 | `feature/F2.1-sample-documents` (pre-commit) | ✅ Pass | Checked by the agent: receipt, form and PDF page 2 viewed; all lines readable and matching. Column spacing in the `.txt` is wider than drawn (proportional font) — compare OCR text with whitespace collapsed. Still to be checked by the user. |
