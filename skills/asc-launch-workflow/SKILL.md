---
name: asc-launch-workflow
description: Orchestrate a complete localized ASC launch or update workflow across ASC metadata, ASC keyword fields, ASC screenshots, and ASC API task JSON. Use when the user wants one coordinated input packet to drive $asc-metadata, $asc-keywords, $asc-screenshots, and $asc-api, including localization lists, writing style, ASO seeds, Pixelmator Pro PXD template paths, screenshot output paths, App Store Connect target identity, artifact handoff, final review, and upload/update preparation.
---

# ASC Launch Workflow

Use this skill as the coordinator for a full ASC launch/update pass:

1. localized metadata copy;
2. localized keyword fields;
3. localized ASC screenshot assets;
4. ASC API task JSON and, after explicit confirmation, optional ASC execution.

Each phase runs in a dedicated subagent to keep the coordinator's context lean. The coordinator builds the shared product brief, dispatches subagents with precise inputs, collects their file outputs and summaries, assembles the review bundle, and handles the ASC mutation confirmation directly with the user. The coordinator never performs the work of a child skill inline.

If any child skill is missing or cannot be loaded, stop before the affected phase and report the missing dependency.

## Security And Live-Update Rules

Never ask the user to paste App Store Connect secrets, `.p8` contents, JWTs, Authorization headers, or `~/.asc_secrets`.

Never read or print `~/.asc_secrets`, `.p8` private keys, tokens, Authorization headers, or full request headers.

Treat App Store Connect writes as a two-step process:

1. Generate final ASC task JSON from reviewed artifacts.
2. Stop and ask the user to confirm the exact JSON before any `POST`, `PATCH`, `DELETE`, upload, submit, or state change.

Read-only ASC discovery may run when the task is clear and local access is available. Mutating ASC operations must never run in the same step that first creates the final JSON unless the user already explicitly approved that exact JSON.

## Start Gate

Before starting any project inspection, subagent dispatch, hard dependency check, file generation, screenshot capture, App Store Connect discovery, or API task drafting, verify that all required inputs for the requested phases are present.

If any required input is missing, do not begin the workflow. Return a concise missing-information checklist and ask the user to provide the missing values. Repeat this gate on the next user response. Continue asking and do not start until every required value for the requested phases is available.

Do not partially execute available phases while waiting for missing required inputs for other requested phases. If the user requested `metadata`, `keywords`, `screenshots`, and `asc-json`, the whole coordinated workflow waits until the required inputs for all four requested phases are complete. Only reduce the required input set when the user explicitly removes phases from scope.

When blocking on missing inputs, use this format:

```markdown
Missing required launch inputs:
- [field]: why it is required

Please provide these values before I start the workflow.
```

## One-Shot Input Packet

When the user wants to provide everything at once, ask for or accept a packet with these sections. Do not require perfect formatting; normalize it into this structure before starting.

```markdown
# ASC Launch Packet

## Project
- Project root:
- App name:
- Bundle ID:
- Platform:
- Category:
- Version string:
- Existing title:
- Existing subtitle:
- Current App Store metadata files:
- Existing screenshot or marketing folders:

## Localizations
- Locales:
- Folder naming style:
- Locale-specific notes:

## Brand And Copy
- Writing style:
- Target audience:
- Core user job:
- 3-5 strongest implemented features:
- Emotional promise:
- Forbidden claims or wording:

## Keywords
- Seed function words per locale:
- Existing title/subtitle words to avoid:
- Competitors per locale:
- App Store autocomplete evidence:
- Trademark/legal-risk preferences:

## Screenshots
- Pixelmator Pro PXD template path:
- Output folder:
- Screenshot device model:
- Screenshot device family and dimensions:
- UI test target/scheme/test plan:
- Desired screenshot page count:
- Required views/states/sample data:
- Existing screenshots, if any:

## App Store Connect
- Intended operation: draft-only | generate-task-json | execute-after-confirmation
- App Store Connect app id, if known:
- ASC resource ids, if known:
- Resource scope: app info | app store version localization | screenshots | mixed
- Target version state, if relevant:
- Fields to update:

## Run Controls
- Phases to run: metadata | keywords | screenshots | asc-json | asc-execute
- Stop after each phase: yes/no
- Save final documents to:
- Human review notes:
```

Minimum required inputs for the full workflow:

- Project root or enough app evidence to understand the product.
- Target localization list.
- Writing style. If missing, ask; default option is `平静内敛`, but the user must choose it or provide another style.
- App category and core user job. Infer both from the project first (README, product docs, existing App Store metadata, app entry point, feature screens). Only ask the user if the project provides insufficient evidence to determine them.
- Keyword seed words or enough user-approved starter context per locale.
- Pixelmator Pro PXD template path and UI test workflow details if `screenshots` is requested.
- ASC app identity or enough local/project evidence for read-only ASC discovery if `asc-json` or `asc-execute` is requested.

Ask only for missing information required by the requested phases. If any required item is missing, stop before all workflow work and request the missing values. Do not inspect the project, run dependency checks, draft copy, generate keyword starters, create folders, or query App Store Connect until the start gate passes.

## Subagent Dispatch Model

Each child skill runs as a subagent. Use whatever subagent mechanism the current environment provides: the Agent tool in Claude Code, named agents in Codex, or any equivalent. The coordinator never performs child-skill work inline.

**Input contract** — every subagent receives:

- the absolute path to `asc-product-brief.md` (written in Step 2);
- the skill name and the specific inputs required by that phase (listed in each step below);
- the output root path so all artifacts land in the same folder tree.

**Output contract** — every subagent must return to the coordinator:

- a one-paragraph completion summary (phase, locales covered, outcome);
- the absolute paths of all files it wrote;
- any blockers, assumptions, or manual follow-up items.

The coordinator records these summaries and paths. It does not re-read the full content of subagent output files unless assembling the review bundle or constructing the next subagent's prompt.

**Error handling** — if a subagent reports a hard blocker, the coordinator stops that phase, reports the blocker to the user, and asks whether to continue with the remaining phases.

## Orchestration Workflow

### 1. Normalize Scope

After the start gate passes, parse the user's packet into:

- requested phases;
- target locales;
- project root;
- output root;
- App Store Connect intent;
- hard blockers.

Create a short run sheet before executing:

```markdown
Run sheet:
- Project:
- Locales:
- Phases:
- Output root:
- ASC mode:
- Stop points:
- Missing inputs:
```

### 2. Build One Shared Product Brief

This step runs in the main conversation, not a subagent. The brief is the shared foundation that all subagents read from file — building it in the main conversation ensures the coordinator fully understands the product before dispatching any work.

Inspect the local project read-only. Prefer README, product docs, existing App Store metadata, localization files, app entry points, feature screens, and screenshot folders.

Produce the brief covering:

- app name, platform, category, target audience;
- core user job;
- 3–5 implemented features with file/evidence hints;
- existing title/subtitle/metadata words;
- brand voice and forbidden claims;
- locale-specific caveats;
- assumptions.

Write the brief to:

```text
<output-root>/asc-product-brief.md
```

All subagents read this file. Do not pass the full brief text in each subagent prompt; pass the file path instead.

### 3. Draft Metadata

Spawn a subagent using `$asc-metadata`.

Pass to the subagent:

- path to `asc-product-brief.md`;
- target locales;
- writing style;
- existing title/subtitle/metadata;
- field scope: `Subtitle`, `Promotional Text`, `App Description`;
- output path: `<output-root>/asc-metadata.md`.

Expect back:

- completion summary;
- path to `asc-metadata.md`.

Do not generate keywords in this phase.

### 4. Draft Keywords

Spawn a subagent using `$asc-keywords`.

Pass to the subagent:

- path to `asc-product-brief.md`;
- path to `asc-metadata.md` (so the subagent can avoid repeating title/subtitle words);
- target locales;
- app category and core user job;
- seed function words per locale;
- competitor/autocomplete evidence when available;
- output path: `<output-root>/asc-keywords.md`.

Expect back:

- completion summary;
- path to `asc-keywords.md`.

### 5. Produce Screenshots

Run this phase only when requested.

Spawn a subagent using `$asc-screenshots`.

Pass to the subagent:

- path to `asc-product-brief.md`;
- target locales and folder naming style;
- PXD template path;
- output folder: `<output-root>/screenshots/`;
- screenshot UI test details (target, scheme, test plan if available).

Note: `$asc-screenshots` internally dispatches its own subagents for promo point discovery and headline writing. The coordinator does not manage those inner subagents; it only waits for the final output.

Expect back:

- completion summary;
- paths to localized screenshot folders;
- paths to generated `.pxd` and `.png` files;
- dependency check result, screenshot acceptance result, export QA result.

Do not let metadata copy automatically become screenshot headlines. Promotional headlines are owned by `$asc-screenshots` and must be grounded in actual screenshots.

### 6. Review Bundle

This step runs in the main conversation. The coordinator reads the output files from Steps 3–5 and assembles a human review bundle. Do not re-execute any child skill here; only read the files already produced.

```markdown
# ASC Launch Review

## Locales

## Metadata

## Keywords

## Screenshots

## Assumptions And Risks

## Manual Checks
```

Check:

- metadata fields fit App Store limits;
- keyword fields are `<= 100` characters and avoid title/subtitle duplication;
- screenshot assets exist and pass QA when requested;
- claims are grounded in project evidence;
- locale names are consistent across metadata, keywords, screenshots, and ASC targets;
- no live ASC mutation has happened yet.

Write the completed review bundle to `<output-root>/asc-launch-review.md`.

Ask the user to review if `Stop after each phase` is enabled or if the bundle contains assumptions that affect live App Store content.

### 7. Generate ASC Task JSON

Run this phase only when requested.

Spawn a subagent using `$asc-api` for task JSON generation only (read-only discovery + JSON drafting, no execution).

Pass to the subagent:

- path to `asc-metadata.md`;
- path to `asc-keywords.md`;
- ASC app identity (bundle ID, app name, or app ID);
- target locales and resource scope;
- target version state if relevant;
- output path: `<output-root>/asc-tasks.json`.

Typical field mappings for the subagent to verify against OpenAPI:

- `Subtitle` → `subtitle`
- `Promotional Text` → `promotionalText`
- `App Description` → `description`
- `Keywords` → `keywords`

Expect back:

- completion summary;
- the full contents of `asc-tasks.json` (the coordinator must show this to the user);
- the matched ASC target summary (App, Bundle ID, Platform, Version, Locale, Resource, ID, Evidence).

After receiving the task JSON, the coordinator shows it to the user in the main conversation and waits for explicit confirmation. Do not proceed to Step 8 until the user confirms the exact JSON shown.

### 8. Execute ASC Tasks

Run this phase only if the user explicitly confirms the exact task JSON from Step 7.

Spawn a subagent using `$asc-api` for execution only.

Pass to the subagent:

- the confirmed `asc-tasks.json` path;
- explicit instruction that this JSON has been user-confirmed and execution is authorized.

Expect back:

- per-task execution summary: method, endpoint path, status code, resource IDs, changed fields;
- any redacted error bodies for failures.

Never print secrets, tokens, Authorization headers, or request headers.

## Output Layout

Prefer a single top-level folder named by the app and date when the user did not provide one:

```text
ASC Launch Assets YYYY-MM-DD/
├── asc-product-brief.md
├── asc-launch-review.md
├── asc-metadata.md
├── asc-keywords.md
├── asc-tasks.json
└── screenshots/
    ├── en-US/
    └── zh-Hans/
```

## Final Response Contract

At the end of a full run, report:

- phases completed;
- output folder path;
- generated metadata and keyword files;
- screenshot asset folders and generated `.pxd`/`.png` files, if any;
- ASC task JSON path or confirmation status;
- hard blockers, assumptions, skipped phases, and manual follow-up;
- whether any live App Store Connect mutation occurred.

Keep the final answer short. The detailed artifact belongs in the generated Markdown report, not the chat.
