# ASC Launch Kit

This repository is a Codex and Claude Code plugin containing Agent Skills for App Store Connect launch/update work.

## Structure

- `.codex-plugin/plugin.json`: Codex plugin manifest.
- `.claude-plugin/plugin.json`: Claude Code plugin manifest.
- `.claude-plugin/marketplace.json`: Claude Code marketplace manifest for installing from this repo.
- `skills/asc-launch-workflow`: top-level coordinator.
- `skills/asc-metadata`: localized ASC listing copy.
- `skills/asc-keywords`: localized ASC keyword fields.
- `skills/asc-screenshots`: localized ASC screenshot assets.
- `skills/asc-api`: safe App Store Connect API automation.
- `skills/pixelmator-pxd-editor`: Pixelmator Pro PXD editing via AppleScript only; used by `asc-screenshots`.
- `scripts/download_openapi.sh`: fetches `openapi.oas.json` from Apple (not committed; run once after cloning).
- `scripts/validate.py`: validates JSON manifests and SKILL.md frontmatter; used by CI and local development.

## Editing Rules

- Keep skill names in directory names and `SKILL.md` frontmatter synchronized.
- Prefer concise skill instructions with progressive disclosure through `references/` and `scripts/`.
- Never commit local ASC credentials, `.p8` files, JWTs, Authorization headers, or `~/.asc_secrets`.
- Never commit `skills/asc-api/references/openapi.oas.json`; it is listed in `.gitignore` and fetched by `scripts/download_openapi.sh`.
- Preserve the strict start gate in `asc-launch-workflow`: missing required inputs means no workflow work starts.
- Preserve the two-step ASC mutation rule: generate final task JSON first, then wait for explicit user confirmation before executing writes.
- Keep `asc-screenshots` focused on screenshot assets, not generic promotional copy.
- Keep `pixelmator-pxd-editor` limited to the official Pixelmator Pro AppleScript dictionary; never add direct PXD package mutation as an allowed path.

## Validation

Run the in-repo validator after any change to plugin manifests or skill files:

```bash
python3 scripts/validate.py
```

For JSON manifests only:

```bash
python3 scripts/validate.py --json
```

For SKILL.md frontmatter only:

```bash
python3 scripts/validate.py --skills
```

If you also have the Codex local plugin validator installed, you can run it as an additional check:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```
