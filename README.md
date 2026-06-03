# ASC Release Kit

[![CI](https://github.com/raydeveloperf/asc-release-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/raydeveloperf/asc-release-kit/actions/workflows/ci.yml)

ASC Release Kit is a Codex and Claude Code plugin for preparing localized App Store Connect updates from real app projects.

It bundles six Agent Skills:

| Skill | Purpose |
| --- | --- |
| `asc-launch-workflow` | Coordinates the full ASC launch/update workflow from one input packet. |
| `asc-metadata` | Writes localized ASC subtitle, promotional text, and app description. |
| `asc-keywords` | Generates localized 100-character ASC keyword fields for ASO. |
| `asc-screenshots` | Produces localized ASC screenshot assets from Xcode UI Test screenshots and Pixelmator Pro PXD templates. |
| `asc-api` | Safely prepares and runs App Store Connect API automation with local credentials and explicit mutation confirmation. |
| `pixelmator-pxd-editor` | Edits, inspects, and exports Pixelmator Pro PXD files through the official AppleScript interface. |

## What It Does

ASC Release Kit is designed for one coordinated App Store Connect publishing flow:

1. Validate that all required launch inputs are present before starting.
2. Build one shared product brief from the local app project.
3. Draft localized metadata.
4. Draft localized keyword fields.
5. Generate localized screenshot assets.
6. Assemble a human review bundle.
7. Generate App Store Connect task JSON.
8. Execute ASC updates only after explicit confirmation of the exact JSON.

The main entry point is `$asc-launch-workflow`.

## Repository Structure

```text
.
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── asc-launch-workflow/
│   ├── asc-metadata/
│   ├── asc-keywords/
│   ├── asc-screenshots/
│   ├── asc-api/
│   └── pixelmator-pxd-editor/
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
└── README.md
```

This follows the common Agent Skills plugin pattern: each skill lives under `skills/<skill-name>/SKILL.md`, with optional `scripts/`, `references/`, and `assets/` folders when needed.

## Install In Claude Code

After publishing this repository to GitHub:

```text
/plugin marketplace add raydeveloperf/asc-release-kit
/plugin install asc-release-kit@asc-release-kit
```

For local development:

```text
/plugin marketplace add /path/to/ASC-Launch-Kit
/plugin install asc-release-kit@asc-release-kit
```

Restart Claude Code after installing or updating the plugin.

## Install In Codex

Codex can use the native plugin manifest in `.codex-plugin/plugin.json` when installed through a Codex plugin host.

For prompt-only local usage, copy or symlink the skill folders into a Codex-discovered skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/asc-* ~/.codex/skills/
cp -R skills/pixelmator-pxd-editor ~/.codex/skills/
```

Then invoke:

```text
$asc-launch-workflow
```

## Required User Inputs

`asc-launch-workflow` has a strict start gate. If required information is missing, it does not inspect the project, run dependency checks, generate drafts, create files, or query App Store Connect.

For a full workflow, provide:

- project root or enough app evidence to understand the product;
- localization list;
- writing style;
- app category and core user job;
- keyword seed words or user-approved starter context per locale;
- Pixelmator Pro PXD template path and UI test workflow details for screenshots;
- ASC app identity or enough evidence for read-only ASC discovery;
- requested phases: `metadata`, `keywords`, `screenshots`, `asc-json`, `asc-execute`.

## Security Model

ASC Release Kit is intentionally conservative around App Store Connect automation.

- Do not paste ASC secrets, `.p8` contents, JWTs, or Authorization headers into chat.
- Keep ASC credentials outside every project, normally in `~/.asc_secrets`.
- Keep `.p8` private keys outside every project, such as under `~/.ssh/`.
- ASC API tokens are generated only inside the local process.
- Read-only ASC discovery can run when the task is clear.
- Mutating ASC operations require the user to confirm the exact generated task JSON first.

The `asc-api` skill includes a safe Python client template and an OpenAPI helper for generating endpoint-aware task JSON.

For a step-by-step guide to generating an API key, creating `~/.asc_secrets`, and verifying your setup, see **[docs/asc-api-setup.md](docs/asc-api-setup.md)**.

## Screenshot Workflow Requirements

`asc-screenshots` requires all of these before it starts:

- Pixelmator Pro installed and AppleScript-addressable;
- a local `.pxd` iPhone mockup template;
- a non-empty target localization list;
- an Xcode UI Test screenshot workflow;
- screenshot acceptance and export QA.

It does not silently replace missing PXD automation with recreated frames or manual screenshots.

## License

MIT. See [LICENSE](LICENSE).
