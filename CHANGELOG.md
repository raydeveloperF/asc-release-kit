# Changelog

All notable changes to ASC Release Kit will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `docs/asc-api-setup.md`: step-by-step guide for generating an App Store Connect API key, storing the `.p8` private key, creating `~/.asc_secrets`, and verifying the setup.
- `asc-screenshots`: new `Writing UI Tests When Missing` section — when no Xcode UI test target exists, the skill inspects the project, generates `ScreenshotTests.swift` and an `.xctestplan` for all target locales, shows the code to the user for approval, writes the files, and runs the tests. Xcode UI Tests remain the only accepted screenshot source.
- `asc-launch-workflow`: new `Subagent Dispatch Model` section defining the input/output contract for all child skill subagents.

### Changed

- `asc-screenshots`: Xcode UI Tests are no longer a hard blocker. Missing tests trigger code generation instead of stopping the workflow. The other four hard dependencies (Pixelmator Pro, AppleScript, PXD template, localization list) remain strict hard stops.
- `asc-screenshots`: subagent delegation decoupled from named agents (`@product-manager`, `@content-marketer`). Any capable subagent is accepted; the platform decides how to spawn it.
- `asc-launch-workflow`: all child skill phases (`$asc-metadata`, `$asc-keywords`, `$asc-screenshots`, `$asc-api`) now run as subagents instead of inline in the main conversation. The coordinator builds the shared product brief in the main conversation, dispatches subagents with file-based inputs, and handles ASC mutation confirmation directly with the user. `asc-product-brief.md` added to output layout as the shared foundation file.

### Changed

- `asc-api` SKILL.md: `Local Credential File` section now directs users to `docs/asc-api-setup.md` instead of describing setup inline.
- README: `Security Model` section links to `docs/asc-api-setup.md`.

## [0.1.0] - 2026-06-03

### Added

- `asc-launch-workflow` — top-level coordinator for a full localized ASC launch or update pass.
- `asc-metadata` — writes localized subtitle, promotional text, and app description with character-count validation.
- `asc-keywords` — generates localized 100-character ASC keyword fields with saturation screening.
- `asc-screenshots` — full screenshot pipeline: UI test capture, Pixelmator Pro PXD editing, PNG export, and visual QA.
- `asc-api` — safe local App Store Connect API client with short-lived JWT signing, two-step mutation confirmation, and bundled OpenAPI spec helper.
- `pixelmator-pxd-editor` — Pixelmator Pro PXD editing exclusively through the official AppleScript dictionary; used by `asc-screenshots`.
- Claude Code plugin manifest (`.claude-plugin/`).
- Codex plugin manifest (`.codex-plugin/`).
- GitHub Actions CI: JSON manifest validation, SKILL.md frontmatter check, Python syntax check, and OpenAPI smoke test.

[Unreleased]: https://github.com/raydeveloperf/asc-release-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/raydeveloperf/asc-release-kit/releases/tag/v0.1.0
