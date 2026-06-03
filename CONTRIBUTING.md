# Contributing to ASC Launch Kit

Thank you for taking the time to contribute. This document covers everything you need to get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Setting Up Your Environment](#setting-up-your-environment)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Bugs](#reporting-bugs)

---

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) code of conduct. By participating, you are expected to uphold this standard. Please report unacceptable behavior to the maintainer via GitHub Issues.

---

## How to Contribute

The most helpful contributions are:

- **Bug reports** — a skill produced wrong output, a script failed, or a manifest caused an install error.
- **Skill improvements** — clearer instructions, better output format, stricter guard rails.
- **New script utilities** — small Python helpers that serve the asc-api workflow.
- **Documentation fixes** — typos, outdated instructions, missing steps.

If you want to add an entirely new skill or significantly change an existing one, please open an issue first so we can discuss the scope.

---

## Setting Up Your Environment

### Requirements

- macOS (the skills are macOS-only by design — they use Xcode, Pixelmator Pro, and Apple APIs)
- Python 3.11 or later
- Claude Code or Codex (to run the skills)

### Steps

1. **Fork and clone**

   ```bash
   git clone https://github.com/raydeveloperf/asc-release-kit.git
   cd asc-release-kit
   ```

2. **Download the OpenAPI spec** (not committed to the repo due to size)

   ```bash
   bash scripts/download_openapi.sh
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r skills/asc-api/scripts/requirements.txt
   ```

4. **Run the validator** to confirm everything is healthy

   ```bash
   python3 scripts/validate.py
   ```

---

## Making Changes

### Repository layout

Each skill lives under `skills/<skill-name>/`:

```
skills/<skill-name>/
├── SKILL.md          ← skill instructions (required)
└── agents/
    └── openai.yaml   ← display name and default prompt (required)
```

The `asc-api` skill also has `scripts/` and `references/` subdirectories.

### Rules to follow

These rules come from [`AGENTS.md`](AGENTS.md) and are enforced by CI:

- Keep the `name` in each `SKILL.md` frontmatter synchronized with the directory name.
- Do not commit `skills/asc-api/references/openapi.oas.json` (it is in `.gitignore`).
- Do not commit ASC credentials, `.p8` keys, JWTs, or Authorization headers — not in skill instructions, scripts, fixtures, or anywhere else in the repo.
- Preserve the strict start gate in `asc-launch-workflow` and the two-step ASC mutation rule in `asc-api`. These are load-bearing safety properties.
- Keep `pixelmator-pxd-editor` limited to the official Pixelmator Pro AppleScript dictionary.

### Validate before pushing

```bash
python3 scripts/validate.py
python3 -m py_compile skills/asc-api/scripts/asc_client.py
python3 -m py_compile skills/asc-api/scripts/inspect_openapi.py
```

---

## Submitting a Pull Request

1. Create a branch from `main`:
   ```bash
   git checkout -b fix/my-description
   ```

2. Make your changes and validate locally (see above).

3. Commit with a clear message:
   ```
   fix(asc-api): correct endpoint path for appInfoLocalizations PATCH
   ```
   Common prefixes: `fix`, `feat`, `docs`, `refactor`, `chore`.

4. Open a pull request against `main`. The PR template will guide you through what to fill in.

5. CI runs automatically. All checks must pass before merge.

---

## Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) issue template. The more detail you provide, the faster the issue can be diagnosed.

**Never include ASC credentials, `.p8` contents, JWTs, or Authorization headers in an issue or pull request.**
