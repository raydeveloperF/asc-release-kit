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

This skill does not replace the four underlying skills. Load and follow each child skill at the relevant step:

- `$asc-metadata` for `Subtitle`, `Promotional Text`, and `App Description`.
- `$asc-keywords` for the hidden 100-character `Keywords` field.
- `$asc-screenshots` for UI test screenshots, Pixelmator Pro PXD editing, PNG exports, and screenshot reports.
- `$asc-api` for App Store Connect discovery, task JSON generation, and safe API execution.

If any child skill is missing or cannot be loaded, stop before the affected phase and report the missing dependency.

## Security And Live-Update Rules

Never ask the user to paste App Store Connect secrets, `.p8` contents, JWTs, Authorization headers, or `~/.asc_secrets`.

Never read or print `~/.asc_secrets`, `.p8` private keys, tokens, Authorization headers, or full request headers.

Treat App Store Connect writes as a two-step process:

1. Generate final ASC task JSON from reviewed artifacts.
2. Stop and ask the user to confirm the exact JSON before any `POST`, `PATCH`, `DELETE`, upload, submit, or state change.

Read-only ASC discovery may run when the task is clear and local access is available. Mutating ASC operations must never run in the same step that first creates the final JSON unless the user already explicitly approved that exact JSON.

## Start Gate

Before starting any project inspection, child-skill execution, hard dependency check, file generation, screenshot capture, App Store Connect discovery, or API task drafting, verify that all required inputs for the requested phases are present.

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
- App category and core user job.
- Keyword seed words or enough user-approved starter context per locale.
- Pixelmator Pro PXD template path and UI test workflow details if `screenshots` is requested.
- ASC app identity or enough local/project evidence for read-only ASC discovery if `asc-json` or `asc-execute` is requested.

Ask only for missing information required by the requested phases. If any required item is missing, stop before all workflow work and request the missing values. Do not inspect the project, run dependency checks, draft copy, generate keyword starters, create folders, or query App Store Connect until the start gate passes.

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

If `screenshots` is requested, run `$asc-screenshots` hard dependency checks before product analysis for screenshot assets. Do not create fallback screenshot assets when Pixelmator Pro, AppleScript automation, PXD template, localization list, or UI tests are missing.

### 2. Build One Shared Product Brief

Inspect the local project read-only unless the user explicitly asks for edits. Prefer README, product docs, existing App Store metadata, localization files, app entry points, feature screens, and screenshot folders.

Produce one shared brief for all child skills:

- app name, platform, category, target audience;
- core user job;
- 3-5 implemented features with file/evidence hints;
- existing title/subtitle/metadata words;
- brand voice and forbidden claims;
- locale-specific caveats;
- assumptions.

Pass this brief into every child skill so metadata, keywords, screenshots, and ASC fields do not drift into four different products wearing the same hat.

### 3. Draft Metadata

Load `$asc-metadata` and follow it strictly.

Inputs to pass:

- shared product brief;
- target locales;
- writing style;
- existing title/subtitle/metadata;
- field scope: `Subtitle`, `Promotional Text`, `App Description`.

Output one Markdown section per locale. Character-count all constrained fields. Save or include the metadata artifact as:

```text
asc-metadata.md
```

Do not generate keywords in this phase.

### 4. Draft Keywords

Load `$asc-keywords` and follow it strictly.

Inputs to pass:

- shared product brief;
- target locales;
- app category and core user job;
- seed function words per locale;
- title/subtitle words from the metadata draft and existing listing;
- competitor/autocomplete evidence when available.

Output ready-to-paste `Keywords` strings under 100 characters per locale. Save or include the keyword artifact as:

```text
asc-keywords.md
```

If evidence is weak, label the keyword sets as starter sets that need manual App Store validation.

### 5. Produce Screenshots

Run this phase only when requested.

Load `$asc-screenshots` and follow it strictly. It owns:

- hard dependency verification;
- product-manager/content-marketer delegation;
- Xcode UI test screenshot capture;
- screenshot acceptance;
- PXD copying and Pixelmator Pro AppleScript editing;
- PNG export;
- final screenshot report.

Pass in:

- shared product brief;
- target locales and folder naming style;
- PXD template path;
- output folder;
- screenshot UI test details;
- metadata/keyword context only where it helps avoid contradictory wording.

Do not let metadata copy automatically become screenshot headlines. Promotional headlines are separate and must be grounded in actual screenshots.

Expected output:

- localized screenshot folders;
- generated `.pxd` and `.png` files;
- promo report with full local absolute paths;
- dependency, screenshot acceptance, export QA, and soft-dependency report.

### 6. Review Bundle

Before any ASC task JSON, assemble a human review bundle:

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

Ask the user to review if `Stop after each phase` is enabled or if the bundle contains assumptions that affect live App Store content.

### 7. Generate ASC Task JSON

Run this phase only when requested.

Load `$asc-api` and follow it strictly.

Use reviewed metadata and keyword artifacts as authoring drafts. Convert them into strict ASC task JSON using the OpenAPI helper from `$asc-api`; do not hand-write schemas from memory.

Typical mappings, subject to OpenAPI verification:

- `Subtitle` -> `subtitle`
- `Promotional Text` -> `promotionalText`
- `App Description` -> `description`
- `Keywords` -> `keywords`

Resolve missing ASC ids through read-only discovery when possible:

1. app by bundle id, app name, or app id;
2. app store version by platform/version/state;
3. localization by locale;
4. screenshot sets by locale/platform/display type when screenshot upload/linking is requested.

Before any mutation, output:

```markdown
Matched ASC target:
- App:
- Bundle ID:
- Platform:
- Version:
- Locale:
- Resource:
- ID:
- Evidence:
```

Then output a JSON array of task objects:

```json
[
  {
    "method": "PATCH",
    "path": "/v1/appStoreVersionLocalizations/RESOURCE_ID",
    "body": {
      "data": {
        "type": "appStoreVersionLocalizations",
        "id": "RESOURCE_ID",
        "attributes": {}
      }
    }
  }
]
```

Stop after showing the final task JSON and ask for explicit confirmation.

### 8. Execute ASC Tasks

Run this phase only if the user explicitly confirms the exact task JSON produced in the previous step.

Use `$asc-api` safe client patterns. Print safe summaries only:

- method and endpoint path;
- status code;
- resource ids and changed fields;
- redacted error bodies when failures occur.

Never print secrets, tokens, Authorization headers, or request headers.

## Output Layout

Prefer a single top-level folder named by the app and date when the user did not provide one:

```text
ASC Launch Assets YYYY-MM-DD/
├── asc-launch-review.md
├── asc-metadata.md
├── asc-keywords.md
├── asc-tasks.json
└── screenshots/
    ├── en-US/
    └── zh-Hans/
```

Use the folder structure required by `$asc-screenshots` inside `screenshots` when generating screenshot assets.

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
