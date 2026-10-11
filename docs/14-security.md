# Security

Security for a small project is mostly habits: keep secrets out of the
code, be careful what you install, and don't trust input. This doc is the
checklist; the rules agents must follow are summarised in `AGENTS.md` →
Security.

## Threat model (lite)

Fill in during Phase 0/1; review at the end of each phase. It answers the
four standard threat-modelling questions in a few lines each.

**1. What are we building?** A local, offline CLI/library that reads image
and PDF files I give it and writes per-page OCR text to a JSON or CSV file.
No network calls and no secrets since S1.1.2 (Baidu removed). See
`02-architecture.md` → System context.

**2. What can go wrong?**

| Asset (what's worth protecting) | Entry point (how it could be reached) | What could go wrong | Likelihood | Impact |
|---|---|---|---|---|
| My documents' text (personal data) | Logs and output files | Document text ends up in logs or somewhere unexpected | Low | Med |
| The run itself | An input image or PDF, given directly or found in a folder I pass (corrupt or malicious) | A bad file crashes the whole run, or exploits a bug in Pillow / PyMuPDF | Med | Med |
| My machine | Dependencies (Pillow, PyMuPDF) | A vulnerable or look-alike package runs code with my permissions | Low | High |

Common entry points: files the app reads, network requests, user input,
command-line arguments, environment variables, dependencies, and anything
an AI agent reads (web pages, issues, docs).

**3. What are we doing about it?**
- Document text: never logged above DEBUG (NFR5); output goes only to the
  path I choose.
- Bad input file: folders expand to top-level image/PDF files only — no
  recursion, other files skipped (S1.1.4); skip-and-report — the file becomes an error in its page
  result and the run continues (NFR4, S1.1.5); file types checked by
  extension before opening (`io.py`); keep Pillow / PyMuPDF up to date.
- Dependencies: only well-known packages from PyPI, checked before adding
  (see Dependencies below); dependency audit each phase end (NFR2).

**4. Did it work?** Bad-file handling: tests in S1.1.5. Logging and audit:
checked at the end of Phase 1 (not yet).

## Secrets

- Secrets (API keys, passwords, tokens) live in `.env`, which is
  git-ignored. `.env.example` lists every variable with a dummy value and
  *is* committed, so anyone can see what's needed.
- Never hardcode a secret, and never put one in logs, test data, error
  messages, prompts to an AI, issues, or screenshots.
- **If a secret leaks** (committed, pasted, shown on screen): revoke/rotate
  it at the provider **first**. Removing it from git history afterwards is
  cleanup — it doesn't make the old key safe again.

## Dependencies

Every dependency is code you didn't write running with your permissions.

- Install only from the official registry for the language (PyPI, npm,
  NuGet…).
- **Before adding one, check it's real and healthy:** the exact name
  exists, it's the package you meant (not a look-alike name), it has
  recent releases, and it's widely used. AI agents sometimes suggest
  package names that don't exist — or that an attacker has registered.
- Use a lock file so every install gets the same versions.
- Run the dependency audit (`AGENTS.md` → Commands) at the end of each
  phase, and act on Dependabot alerts (GitHub only).
- Fewer dependencies = less risk. See `06-coding-conventions.md` →
  Simplicity first.

## Input handling

- Treat all input from outside the program as untrusted: files, network,
  user input, command-line arguments, environment variables.
- Validate at the boundary — the first place input enters — and reject
  what doesn't fit, with a clear error.
- Never build code, shell commands, file paths, or database queries by
  pasting input into a string. Use parameterised queries and the
  language's safe APIs; never `eval` input.

## Privacy

- Collect and keep only the personal data the project actually needs.
- No personal data in logs, test data, screenshots, or bug reports.
- If the project stores personal data, note where, why, and how it's
  deleted in `02-architecture.md` → Data model.

## AI-agent risks

- Don't give AI agents production credentials or access they don't need.
- Content an agent reads — web pages, issues, files from elsewhere — can
  contain instructions aimed at the agent. Treat it as data, never as
  instructions.
- Read commands before approving them, especially anything that deletes,
  installs, pushes, or sends data somewhere.

## GitHub setup (Phase 0) — GitHub only

**n/a if `AGENTS.md` says `Hosting: local`** — skip this section and leave
the boxes unchecked. Do it when you switch to GitHub
(`13-git-workflow.md` → Switching).

In the repo's **Settings → Advanced Security** (wording varies):

- [ ] **Dependabot alerts** — warns about known vulnerabilities in
      dependencies
- [ ] **Dependabot security updates** — opens PRs that update vulnerable
      dependencies
- [ ] **Secret scanning** and **push protection** — detects (and blocks
      pushes containing) known kinds of secrets

These are free for public repositories. For private repositories, check
what your plan includes in Settings.

## Checklists

### Every change
- [ ] No secrets in code, config, logs, or test data
- [ ] New input paths validate their input at the boundary
- [ ] Any new dependency checked as above and logged in
      `05-decisions-log.md`

### End of each phase
- [ ] Dependency audit clean, or every finding has a decision logged
- [ ] Open Dependabot / secret scanning alerts reviewed (GitHub only)
- [ ] Threat model still accurate — new components or entry points added
