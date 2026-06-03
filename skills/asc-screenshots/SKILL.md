---
name: asc-screenshots
description: Create localized ASC screenshots for iOS apps from a real project, Xcode UI Test screenshots, and a Pixelmator Pro PXD iPhone mockup template. Use when the user asks for App Store Connect screenshots, ASC screenshot assets, localized screenshot generation, hard dependency checks, product angle discovery, Xcode UI Test screenshot capture, localized short headlines, Pixelmator Pro AppleScript PXD editing, visual QA, and PNG export.
---

# ASC Screenshots

Use this skill to run the full ASC screenshot pipeline: product angles -> UI screenshots -> localized headline copy -> Pixelmator Pro PXD files -> PNG exports.

## Hard Dependencies

Before starting, verify all five hard dependencies:

- Pixelmator Pro is installed and launchable.
- Pixelmator Pro AppleScript automation is available.
- A local `.pxd` file that contains the iPhone mockup/template.
- The target localization language list.
- Xcode UI Tests are available for the target iOS project screenshot workflow.

If any hard dependency is missing, stop before product analysis, screenshots, PXD creation, or fallback asset work. Tell the user the workflow requires all five hard dependencies and list exactly which ones are missing. Do not substitute manual screenshots, a recreated iPhone frame, non-PXD templates, or non-AppleScript PXD edits for missing hard dependencies.

Hard dependency verification checklist:

- Pixelmator Pro: confirm the app is installed and can be launched or addressed by AppleScript.
- Pixelmator Pro AppleScript: run a minimal read-only AppleScript check, such as reading `name` or `build number`, without opening or changing user documents.
- PXD template: confirm the user-provided path exists, has a `.pxd` extension, and is a local file intended to contain the iPhone mockup.
- Localization list: confirm the list is non-empty, normalize each language to a stable output folder name, and ask before inventing missing locales.
- Xcode UI Tests: confirm the project has a runnable UI test target, scheme, or test plan for the screenshot workflow, and that the tests can produce screenshots either as files in the output tree or as test attachments that can be extracted.

## Soft Dependencies

Other skills and named subagents are soft dependencies:

- If `$pixelmator-pxd-editor`, `$ui-ux-pro-max`, or `$imagegen` is available locally, use it for its relevant step.
- If a soft skill is unavailable, skip that skill-specific pass or use the closest safe local substitute, then report at the end that the workflow did not follow the most standard path and name the substitute used.
- Prefer `@product-manager` and `@content-marketer` for their named roles when available.
- If a named subagent is unavailable, spawn the closest substitute subagent for that role with the same constraints.
- Delegation itself is mandatory: do not perform product-manager or content-marketer work in the main conversation. If no subagent mechanism is available at all, stop and report that the workflow is blocked by missing subagent delegation.

Soft dependency resolution:

- Treat a skill as available only when it appears in the current skill metadata or was explicitly provided by the user, and its `SKILL.md` can be loaded.
- Load an available soft skill before the relevant step, then follow the narrower skill when it conflicts with general guidance here.
- Treat a subagent as available when the current environment exposes a way to spawn an agent by name, role, or close task description.
- When substituting a named subagent, keep the original prompt constraints and record the substitute role/name for the final report.
- Do not use soft-dependency fallback to bypass any hard dependency.

## Non-Negotiable PXD Rules

- When editing, inspecting, automating, or exporting PXD files, use `$pixelmator-pxd-editor` if it is available; otherwise follow the Pixelmator Pro AppleScript rules in this skill and report the soft-dependency fallback at the end.
- Treat the provided PXD as a template only.
- Never modify the template in place.
- Copy the template into the output language folder for each generated promo file, then edit only the copy.
- Use the iPhone mockup from the template. Do not recreate the device frame unless the user explicitly asks for a fallback.
- Edit PXD files and export PNG files only through Pixelmator Pro's official AppleScript dictionary.
- Do not generate final PXD files by mutating PXD zip contents, SQLite metadata, QuickLook previews, thumbnails, or `data/*OriginalContentSource` files directly.
- If Pixelmator Pro cannot open the copied PXD, stop the PXD/PNG step and report the invalid template.

## Subagent Delegation

This is a multi-agent workflow. When this skill is invoked, treat that as an explicit request to use subagents. The named subagents are preferred soft dependencies, but the work must still be delegated to a subagent if the exact name is unavailable.

Default delegation:

- Spawn `@product-manager` after hard dependencies are confirmed and before screenshot planning.
- If `@product-manager` is unavailable, spawn the closest product strategy or app marketing substitute subagent with the same prompt.
- Spawn `@content-marketer` after promo points and screenshot inventory exist and before editing PXD headlines.
- If `@content-marketer` is unavailable, spawn the closest copywriting or localization marketing substitute subagent with the same prompt.

Do not silently perform these roles in the main conversation just because the parent agent can. If no subagent mechanism is available at all, stop and report that subagent delegation is required.

Use concise prompts:

`@product-manager`:

```text
Inspect this app project and identify App Store promotional angles. Return a short table with: promo point, concrete view/screen to screenshot, required UI state or sample data, and why this is worth promoting. Keep claims grounded in the current project. Do not edit files.
```

`@content-marketer`:

```text
Using the confirmed promo points, screenshots, and target localizations, write one short localized headline per promo point. Default to one phrase/sentence; English around 5-6 words, other languages similarly compact. Keep claims grounded in the app and screenshot state. Do not edit files unless explicitly asked.
```

## Screenshot Acceptance Criteria

Before creating PXD files, every screenshot must pass these checks:

- One screenshot exists for each selected promo point and localization.
- The active UI language, region-sensitive text, and screenshot folder match the target localization.
- The screenshot shows the requested app view, deterministic state, and sample data from the promo plan.
- The screenshot contains no loading spinners, empty/error states, keyboard overlap, debug overlays, simulator chrome, or accidental system alerts.
- The screenshot orientation, device family, and pixel dimensions fit the PXD template's intended screen placeholder.
- The file is non-empty, visually non-blank, and named with the promo order and stable slug.

If a screenshot fails acceptance, recapture it before editing PXD files. If it cannot be recaptured through Xcode UI Tests, stop and report the blocked screenshot.

## Workflow

1. Confirm workspace and outputs.
   - Verify the five hard dependencies first; stop and list missing items if any are unavailable.
   - Resolve the iOS project root and the provided PXD path.
   - Normalize localization folder names, such as `en：英语` or `zh-Hans：简体中文`, following the user's naming style when provided.
   - Create one top-level output folder at the outermost project root, for example `App Store Promo Assets/`.

2. Identify promo points.
   - Delegate to `@product-manager` when available, or to the closest substitute product/app marketing subagent when it is not.
   - Require concrete screenshot needs: app view, state, data setup, and claim.
   - Keep claims grounded in implemented product behavior.

3. Capture localized screenshots.
   - Use Xcode UI Tests for iOS screenshots.
   - Use XcodeBuildMCP tooling when available to build, run, and capture through the UI test workflow; otherwise run the Xcode UI Tests through the available local Xcode tooling and report the substitute path at the end.
   - For many localizations, consider an Xcode Test Plan for the language/region matrix.
   - Generate deterministic UI states required by the promo points.
   - Export or extract UI test screenshots into the language screenshot folders.
   - Apply the screenshot acceptance criteria before moving to PXD creation.
   - Save screenshots under one folder per language:
     - `App Store Promo Assets/en：英语/screenshots/`
     - `App Store Promo Assets/zh-Hans：简体中文/screenshots/`
   - Name screenshots by promo point, such as `01-memory-timeline.png`.

4. Write localized headlines.
   - Delegate to `@content-marketer` when available, or to the closest substitute copywriting/localization marketing subagent when it is not.
   - Default to one compact phrase or sentence; English around 5-6 words, other languages similarly short.
   - Do not invent features or claims not visible in the app/project.

5. Create PXD files.
   - Load and follow `$pixelmator-pxd-editor` before any PXD inspection, editing, automation, or export when it is available.
   - If `$pixelmator-pxd-editor` is unavailable, continue only with Pixelmator Pro's official AppleScript dictionary and report the fallback at the end.
   - For each language and promo point, copy the PXD template into that language folder.
   - Default file names are `page1.pxd`, `page2.pxd`, etc., unless the user asks otherwise.
   - Open each copied PXD through Pixelmator Pro AppleScript only after copying.
   - Replace the iPhone screen image with the matching UI screenshot using Pixelmator Pro's `replace image` command.
   - Preserve template layer adjustments, effects, styles, masks, position, and layout.
   - If the template has a headline/text placeholder, replace only that text and preserve its position, size, style, and layout.
   - If no headline placeholder exists, place short headline text where it fits without covering the device or important UI.

6. Decide on decoration.
   - Use `$ui-ux-pro-max` as a design review pass before adding decoration when it is available.
   - Skip decoration when the template already looks balanced.
   - If `$ui-ux-pro-max` is unavailable, make a minimal local visual judgment and report the fallback at the end.
   - If decoration helps and `$imagegen` is available, use `$imagegen` for subtle background assets that match the app design language.
   - If decoration helps but `$imagegen` is unavailable, skip generated decoration or use existing project/template assets only, then report the fallback at the end.
   - Keep decoration quiet: modest saturation, simple shapes, no busy detail, never competing with the app UI or headline.
   - Place background assets behind the iPhone/mockup and text.

7. Final QA and export.
   - Use `$ui-ux-pro-max` for final visual review of PXD previews/exports when it is available.
   - If `$ui-ux-pro-max` is unavailable, perform a basic local QA pass and report the fallback at the end.
   - Check headline fit, screenshot fit, language folder organization, contrast, hierarchy, and the export QA checklist.
   - Export PNG files next to their PXD files in the same language folder.
   - Report generated folders and any screenshots/PXD files that could not be produced.
   - Report any unavailable soft dependencies, substitute subagents, skipped soft-skill steps, and whether the result followed the most standard path.

Export QA checklist:

- Each expected `.pxd` and `.png` exists in the correct language folder and is non-zero size.
- Each language has the same page count and matching promo order unless the user requested otherwise.
- PNG dimensions match the edited PXD canvas and the intended App Store screenshot size.
- The inserted app screenshot is visible, correctly clipped, and not stretched into the wrong aspect ratio.
- Headlines fit without clipping, overlap, low contrast, or awkward line breaks in every localization.
- Device mockup, text, and optional decoration preserve the template hierarchy and do not cover important app UI.
- The original PXD template timestamp or checksum is unchanged when that can be checked cheaply.

## Pixelmator Pro AppleScript Pattern

When available, use `$pixelmator-pxd-editor` as the source of truth for PXD inspection, editing, allowed AppleScript commands/properties, safety defaults, and export behavior. If it is unavailable, follow this section directly and report the fallback at the end.

Use Pixelmator Pro's official AppleScript automation for all editable PXD work:

- Use `open` for copied PXD files.
- Use layer names and recursive group traversal to find text/image placeholders.
- Use `replace image ... with ... scale mode scale to fill` or `scale to fit` for screen replacement.
- Use `replace text` for known placeholder text, or set a matched text layer's `text content`.
- Use `save as new document ... as Pixelmator Pro` for the edited PXD copy.
- Use `export ... as PNG` for final PNG output.
- Restore `autosave enabled` after scripts that change it.
- Close only the document opened by the script, using `saving no`; do not close unrelated user documents.

Verified safe shape for common iPhone mockup templates:

```applescript
set copiedPXD to POSIX file "/path/to/copied-template.pxd"
set screenshotFile to POSIX file "/path/to/screenshot.png"
set outputPXD to POSIX file "/path/to/output/page1.pxd"
set outputPNG to POSIX file "/path/to/output/page1.png"
set headlineText to "A calmer way to journal"

tell application "Pixelmator Pro"
  activate
  set oldAutosave to autosave enabled
  set autosave enabled to false

  set promoDoc to open copiedPXD
  delay 1

  tell promoDoc
    set text content of text layer "Headline" to headlineText

    set phoneGroup to group layer "iPhone 16 Pro"
    set screenLayer to image layer "Media Placeholder: Replace With Your Media" of phoneGroup
    replace image screenLayer with screenshotFile scale mode scale to fill

    save as new document it in outputPXD as Pixelmator Pro
    export it to outputPNG as PNG
  end tell

  close promoDoc saving no
  set autosave enabled to oldAutosave
end tell
```

Do not assume these exact layer names. Inspect the copied PXD first, then adapt layer names while preserving the same safe copy/open/edit/save/export structure.

## Output Contract

At completion, return:

- The top-level output folder path.
- A final Markdown report file in the top-level output folder. The report must be grouped by language, include the screenshot device model for each promo point, such as `iPhone 17 Pro`, and show every screenshot as its full local absolute path.
- A per-language list of generated `.pxd` and `.png` files.
- A short note on how screenshots were captured.
- A hard dependency check result.
- A screenshot acceptance result.
- An export QA result.
- A soft dependency/delegation report: used, substituted, skipped, and whether the workflow followed the most standard path.
- Any manual follow-up needed, such as simulator setup, missing localization, or unsupported template layer structure.
