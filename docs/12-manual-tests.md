# Manual tests

Checks that automated tests can't judge well — how something looks, feels,
or plays, or whether it's actually usable. Write the steps once per feature,
then record a result each time you run them. Run them before marking a
feature done (`07-testing-checklist.md`) and again before closing a phase.

If a manual check finds a bug, log it in `01-requirements.md` → Bugs, and
add an automated test for it if one is possible.

---

## <Feature ID> — <Feature title>

**What to check:** <the things only a person can judge — e.g. "movement
feels responsive", "the chart is readable at a glance">

**Steps:**
1. <setup / starting state>
2. <action>
3. <what you should see>

**Results:**

| Date | Version / commit | Result | Notes |
|---|---|---|---|
| YYYY-MM-DD | <short commit hash> | ✅ Pass / ❌ Fail | <what you saw; bug ID if it failed> |

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

---

## Template

```
## <Feature ID> — <Feature title>

**What to check:** <...>

**Steps:**
1. <...>

**Results:**

| Date | Version / commit | Result | Notes |
|---|---|---|---|
```
