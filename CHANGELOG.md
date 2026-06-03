# Changelog

All notable changes to ASC Release Kit will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `docs/asc-api-setup.md`: step-by-step guide for generating an App Store Connect API key, storing the `.p8` private key, creating `~/.asc_secrets`, and verifying the setup.

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
