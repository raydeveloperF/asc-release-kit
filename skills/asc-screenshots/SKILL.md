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
- Xcode UI Tests are available for the target iOS project screenshot workflow, **or the project is inspectable so that UI test code can be generated**.

If Pixelmator Pro, its AppleScript support, the PXD template, or the localization list are missing, stop immediately. Tell the user which of those four items is missing. Do not substitute manual screenshots, a recreated iPhone frame, non-PXD templates, or non-AppleScript PXD edits for any of these four missing items.

Xcode UI Tests follow a different rule: if they are missing, do not stop. Instead follow the `Writing UI Tests When Missing` section to inspect the project, generate a working screenshot test target, write it into the project, confirm it with the user, and run it. Only stop if the project cannot be read or understood well enough to write meaningful test navigation.

Hard dependency verification checklist:

- Pixelmator Pro: confirm the app is installed and can be launched or addressed by AppleScript.
- Pixelmator Pro AppleScript: run a minimal read-only AppleScript check, such as reading `name` or `build number`, without opening or changing user documents.
- PXD template: confirm the user-provided path exists, has a `.pxd` extension, and is a local file intended to contain the iPhone mockup.
- Localization list: confirm the list is non-empty, normalize each language to a stable output folder name, and ask before inventing missing locales.
- Xcode UI Tests: check whether a UI test target already exists in the project. If it exists and has screenshot-capable tests, use them directly. If it does not exist or has no screenshot tests, proceed to `Writing UI Tests When Missing`.

## Writing UI Tests When Missing

When no Xcode UI test target exists for the project, or the existing UI test target has no screenshot-capturing tests, generate and add them before running the screenshot workflow. Follow this process exactly.

### 1. Inspect the project

Read the project read-only to understand the app structure before writing any test code:

- Identify the main app target name and bundle ID from the `.xcodeproj` or `Package.swift`.
- Find the app entry point: `@main`, `App` conformance, `SceneDelegate`, or `AppDelegate`.
- Find the key screens to promote: main views, tab bar structure, navigation hierarchy, and any feature-specific screens confirmed by the promo plan.
- Note any existing launch arguments or `ProcessInfo.processInfo.environment` checks the app already uses for testing or preview modes. Use the same pattern to inject screenshot state.
- Check for existing sample data or test fixtures that produce realistic content. Prefer them over empty-state screenshots.

### 2. Create a UI test target if one does not exist

If the project has no UI test target at all, create one:

1. Add a new target of type **UI Testing Bundle** in Xcode. Name it `<AppName>UITests` following the existing naming convention.
2. Set the **Target to be Tested** to the main app target.
3. Add the new target to the existing scheme under **Test → Test**.
4. Create the test file at `<AppName>UITests/<AppName>ScreenshotTests.swift`.

If the project already has a UI test target but no screenshot tests, add a new file `ScreenshotTests.swift` inside the existing target. Do not modify existing test files.

### 3. Write the screenshot test file

Generate a `ScreenshotTests.swift` file tailored to this app's navigation. Use this structure as the base pattern:

```swift
import XCTest

final class ScreenshotTests: XCTestCase {

    private var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        // Use a launch argument so the app can detect screenshot mode
        // and load deterministic sample data if it supports this.
        app.launchArguments += ["--screenshot-mode"]
        app.launch()
    }

    // Add one test function per promo point.
    // Name each test with a two-digit prefix so they sort by capture order.
    func test01_MainScreen() throws {
        // The app launches directly to the main screen.
        // Wait for the UI to settle before capturing.
        XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))
        capture(name: "01-main-screen")
    }

    func test02_DetailView() throws {
        // Navigate to the detail view.
        app.buttons["Add Entry"].firstMatch.tap()
        XCTAssertTrue(app.navigationBars.firstMatch.waitForExistence(timeout: 3))
        capture(name: "02-detail-view")
    }

    // MARK: - Helper

    private func capture(name: String) {
        let screenshot = XCUIScreen.main.screenshot()

        // Store as XCTAttachment so it is always preserved in the result bundle.
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)

        // Also write directly to a folder so extraction is straightforward.
        // Pass SCREENSHOT_OUTPUT_DIR as an environment variable when running tests
        // if direct file output is preferred over xcresulttool extraction.
        if let outputDir = ProcessInfo.processInfo.environment["SCREENSHOT_OUTPUT_DIR"] {
            let dir = URL(fileURLWithPath: outputDir)
            try? FileManager.default.createDirectory(at: dir,
                                                     withIntermediateDirectories: true)
            let file = dir.appendingPathComponent("\(name).png")
            try? screenshot.pngRepresentation.write(to: file)
        }
    }
}
```

Adapt the test body for each promo point identified in the promo plan. Replace the example navigation steps with real element queries derived from the inspected app. Use `waitForExistence(timeout:)` instead of `sleep` for all waits.

Do not invent UI element labels. Derive them from the inspected source: `accessibilityIdentifier`, `accessibilityLabel`, button titles, navigation bar titles, or visible text strings from the app's localization files.

### 4. Handle localization in tests

To capture screenshots in multiple languages, use an Xcode Test Plan:

1. Create `<AppName>Screenshots.xctestplan` at the project root.
2. Add one configuration per locale. Example for two locales:

```json
{
  "configurations": [
    {
      "id": "en-US-config",
      "name": "en-US",
      "options": {
        "language": "en",
        "region": "US"
      }
    },
    {
      "id": "zh-Hans-config",
      "name": "zh-Hans",
      "options": {
        "language": "zh-Hans",
        "region": "CN"
      }
    }
  ],
  "defaultOptions": {
    "testTimeoutsEnabled": true,
    "defaultTestExecutionTimeAllowance": 60
  },
  "testTargets": [
    {
      "target": {
        "name": "<AppName>UITests",
        "type": "target"
      }
    }
  ],
  "version": 1
}
```

3. Add the test plan to the scheme under **Test → Test Plans**.

If a test plan already exists in the project for other targets, add a new test plan rather than modifying the existing one.

### 5. Show the generated code to the user before writing

Before writing any file to the project, show the user:

- The full `ScreenshotTests.swift` content.
- The test plan JSON, if generated.
- The target and scheme changes needed.

Ask for confirmation. If the user requests changes to the navigation steps, update the generated code. Do not write to the project until the user approves.

**After the user approves, immediately write the files and proceed to step 6 (run the tests). Do not stop or summarize after writing. Approval is authorization to execute the full remaining pipeline: write → build → run → extract → PXD → PNG.**

### 6. Run the tests and extract screenshots

After the user approves and the files are written, run the tests using XcodeBuildMCP when available, or via `xcodebuild` directly:

```bash
# With a test plan for all locales at once:
xcodebuild test \
  -project <AppName>.xcodeproj \
  -scheme <SchemeName> \
  -testPlan <AppName>Screenshots \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  -resultBundlePath TestResults.xcresult

# Extract screenshots from the result bundle:
xcrun xcresulttool get --path TestResults.xcresult \
  --format json > result.json
```

If `SCREENSHOT_OUTPUT_DIR` was set, screenshots are already in that folder; skip extraction.

To extract attachments from an `.xcresult` bundle without writing a custom parser, use:

```bash
# List all attachments
xcrun xcresulttool export --path TestResults.xcresult \
  --output-path screenshots/ \
  --type directory
```

Organize extracted screenshots into the per-language folder structure required by the rest of this workflow before continuing to screenshot acceptance.

### 7. Note the generated tests in the output report

At the end of the workflow, the output report must include:

- Whether UI tests were pre-existing or generated by this skill.
- The file path of any generated `ScreenshotTests.swift` and test plan.
- The exact `xcodebuild` command used to run them.
- Whether `--screenshot-mode` was supported by the app or was passed as an unused launch argument.

## Soft Dependencies

`$pixelmator-pxd-editor` is a soft dependency for PXD editing. Use it when available; otherwise follow the AppleScript rules in this skill directly and note the fallback in the output report.

`$ui-ux-pro-max` and `$imagegen` are not part of this toolkit. Do not reference or wait for them.

## Non-Negotiable PXD Rules

- When editing, inspecting, automating, or exporting PXD files, use `$pixelmator-pxd-editor` if it is available; otherwise follow the Pixelmator Pro AppleScript rules in this skill and report the soft-dependency fallback at the end.
- Treat the provided PXD as a template only.
- Never modify the template in place.
- Copy the template into the output language folder for each generated promo file, then edit only the copy.
- Use the iPhone mockup from the template. Do not recreate the device frame unless the user explicitly asks for a fallback.
- Edit PXD files and export PNG files only through Pixelmator Pro's official AppleScript dictionary.
- Do not generate final PXD files by mutating PXD zip contents, SQLite metadata, QuickLook previews, thumbnails, or `data/*OriginalContentSource` files directly.
- If Pixelmator Pro cannot open the copied PXD, stop the PXD/PNG step and report the invalid template.
- **If a PXD template path was provided, the PXD processing step is mandatory and must be completed before reporting success.** Do not silently skip PXD creation and output only raw screenshots. If Pixelmator Pro cannot be launched, cannot be addressed via AppleScript, or fails to process the template, stop immediately and report the exact failure. Raw Xcode UI test screenshots are an intermediate artifact, not a finished deliverable when a PXD template path is present.

## Subagent Delegation

Two workflow steps must be delegated to subagents: promo point discovery (Step A) and headline writing (Step B). Use whatever subagent mechanism the environment provides. If none exists, perform both inline and note it in the output report.

**Step A — Promo point discovery**

Run after hard dependencies are confirmed, before screenshot planning. Spawn a subagent capable of product strategy or app marketing analysis with this prompt (substitute actual values):

```text
You are helping plan App Store screenshots for an iOS app.
Project path: <project_root>

Inspect the project read-only and identify the best App Store promotional angles.
Return a table with these columns:
- Promo point: the feature or value being showcased
- Screen to capture: the exact view or state to screenshot
- Required UI state or sample data: what must be visible before the screenshot
- Why it's worth promoting: one sentence grounded in the actual project

Identify 3–6 promo points. Keep all claims grounded in what is implemented. Do not edit any files.
```

**Step B — Localized headline writing**

Run after promo points and screenshots exist, before PXD editing. Spawn a subagent capable of localized marketing copywriting with this prompt (substitute actual values):

```text
You are writing App Store screenshot headlines for an iOS app.
Promo points: <promo_point_table>
Target locales: <locale_list>

Write one short headline per promo point per locale.
- Default length: one phrase or sentence, around 5–6 words in English, similarly compact in other languages.
- Write in the target language natively, not translated English.
- Keep all claims grounded in the confirmed promo points and visible app state.
- Do not invent features or make claims unsupported by the screenshots.
- Do not edit any files.

Return a table grouped by locale: locale | promo point | headline.
```

Record which subagent or agent type was used for each step in the final output report.

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
   - Determine the top-level output folder: if the caller provided an output folder path, use that exactly. Otherwise create `App Store Promo Assets/` at the outermost project root.

2. Identify promo points.
   - Delegate to a subagent capable of product strategy or app marketing analysis, following the Step A prompt in `Subagent Delegation`.
   - Require concrete screenshot needs: app view, state, data setup, and claim.
   - Keep claims grounded in implemented product behavior.

3. Capture localized screenshots.
   - Check whether a screenshot-capable UI test target already exists in the project.
   - If it does not exist, follow `Writing UI Tests When Missing` in full before continuing: inspect the project, generate `ScreenshotTests.swift` and a test plan, show the code to the user, wait for approval, write the files, **then immediately run the tests**. Do not stop after writing.
   - If it already exists, verify it can produce the promo-point screenshots the plan requires. Add missing test functions if needed, following the same show-and-confirm rule before writing, then immediately run.
   - Use XcodeBuildMCP tooling when available to build, run, and capture; otherwise use `xcodebuild` directly.
   - Run tests with the generated test plan to cover all locales in one pass.
   - Export or extract UI test screenshots from the result bundle into the language screenshot folders.
   - Apply the screenshot acceptance criteria before moving to PXD creation.
   - Save screenshots under one folder per language inside the top-level output folder:
     - `<output-folder>/en：英语/screenshots/`
     - `<output-folder>/zh-Hans：简体中文/screenshots/`
   - Name screenshots by promo point, such as `01-memory-timeline.png`.

4. Write localized headlines.
   - Delegate to a subagent capable of localized marketing copywriting, following the Step B prompt in `Subagent Delegation`.
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

6. Final QA and export.
   - Check headline fit, screenshot fit, language folder organization, contrast, and hierarchy against the export QA checklist.
   - Export PNG files next to their PXD files in the same language folder.
   - Report generated folders and any screenshots/PXD files that could not be produced.

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
