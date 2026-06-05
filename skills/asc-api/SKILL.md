---
name: asc-api
description: Safely automate ASC through the official App Store Connect REST API from macOS using project-external local credentials, short-lived local JWT signing, and the bundled OpenAPI spec. Use when the user asks Codex to inspect, create, update, delete, or script App Store Connect resources such as apps, builds, versions, metadata, pricing, analytics reports, beta testing, certificates, identifiers, profiles, or any ASC endpoint. Also use when generating local Python automation that must never expose ASC API keys, .p8 private keys, JWTs, Authorization headers, or ~/.asc_secrets.
---

# ASC API

Use this skill to build or run local App Store Connect automation without exposing secrets to Codex, logs, repositories, or remote model context.

The default pattern is:

1. Keep credentials outside every project in `~/.asc_secrets`.
2. Keep the `.p8` private key outside every project, such as under `~/.ssh/`.
3. Generate a 20-minute JWT only inside the local Python process.
4. Send requests directly to `https://api.appstoreconnect.apple.com/`.
5. Print only safe response summaries, never tokens or request headers.

## Hard Security Rules

Never ask the user to paste `ASC_KEY_ID`, `ASC_ISSUER_ID`, `.p8` contents, JWTs, or `Authorization` headers into chat.

Never run commands that reveal secrets, including:

- `cat ~/.asc_secrets`
- `cat *.p8`
- `printenv`
- `env`
- any command that prints `ASC_*`, `PRIVATE KEY`, `Bearer`, or `Authorization`

Never add real credentials to a project file, git-tracked file, script, fixture, markdown doc, shell history snippet, or test output.

Never print `token`, `auth_headers`, `response.request.headers`, `PreparedRequest.headers`, or full request dumps. On failures, print only:

- HTTP method and endpoint path
- status code
- response body text or JSON
- redacted diagnostics such as `Authorization: <redacted>`

If authentication, signing, missing-file, missing-field, permission, or ASC `401`/`403` errors occur, tell the user to manually inspect `~/.asc_secrets` and the `.p8` path on their own machine. Explicitly state that Codex cannot and should not access the user's secret file, private key, JWT, or Authorization header.

For mutating live ASC operations (`POST`, `PATCH`, `DELETE`), confirm the target app/resource and intended changes with the user before executing. After generating final task JSON, stop and show it to the user. Do not upload or modify App Store Connect until the user explicitly confirms that final JSON. For read-only `GET`, proceed when the task is clear.

## Local Credential File

Expect the user to create this file manually outside the project. If they have not done so yet, direct them to **`docs/asc-api-setup.md`** in the repository root for a complete step-by-step guide covering key generation, `.p8` file storage, and setup verification.

The file location:

```text
~/.asc_secrets
```

Expected keys:

```text
ASC_KEY_ID=YOUR_KEY_ID
ASC_ISSUER_ID=YOUR_ISSUER_ID
ASC_KEY_PATH=/Users/YOUR_USERNAME/.ssh/AuthKey_XXXXXX.p8
```

The skill may create code that reads these fields, but must not inspect or print the file.

Required Python packages:

```bash
pip3 install requests pyjwt cryptography
```

If dependencies are missing, tell the user the install command. Do not install packages unless the user asked for execution or approved the action.

## Bundled Resources

- `references/openapi.oas.json`: complete App Store Connect OpenAPI specification (~6 MB, **not committed to the repository**). Fetch it by running `bash scripts/download_openapi.sh` from the repo root before using this skill. If the file is missing, tell the user to run that script first.
- `scripts/inspect_openapi.py`: local helper for listing/searching endpoints in the bundled OpenAPI spec.
- `scripts/asc_client.py`: safe local Python client template for JWT generation and ASC requests.
- `scripts/requirements.txt`: Python dependencies — install with `pip install -r skills/asc-api/scripts/requirements.txt`.

Use the helper instead of loading the whole 6MB OpenAPI file into context:

```bash
python3 asc-api/scripts/inspect_openapi.py search appStoreVersions
python3 asc-api/scripts/inspect_openapi.py path /v1/apps
python3 asc-api/scripts/inspect_openapi.py operations GET /v1/apps
python3 asc-api/scripts/inspect_openapi.py template PATCH /v1/appStoreVersionLocalizations/{id}
```

Use `template` to generate task JSON skeletons directly from the bundled OpenAPI `requestBody` schema. Prefer generated templates over hand-written assumptions, because ASC field ownership differs by resource. For example, this OpenAPI spec places `keywords` under `appStoreVersionLocalizations` update attributes.

## Markdown to Task JSON

When the user provides App Store Connect update content in Markdown, treat the Markdown as an authoring draft, not as an executable payload.

The Markdown format may be loose. Codex should extract intent from natural headings, labels, and prose, then convert it into strict ASC task JSON using the OpenAPI-generated template.

Useful Markdown anchors include:

```markdown
# App Store Connect Update

Resource: appStoreVersionLocalizations
ID: 123456789
Locale: zh-Hans

## Promotional Text

更安静地记录每一天。

## Keywords

日记,情绪,照片,记录,生活

## What's New

- 优化了记录体验
- 修复了一些细节问题
```

The anchors do not need to be exact. Map common human labels to ASC attribute names when the OpenAPI schema confirms the target resource supports them:

- `宣传文本`, `Promotional Text`, `promotional text` -> `promotionalText`
- `关键词`, `Keywords`, `keyword` -> `keywords`
- `更新说明`, `What's New`, `Release Notes` -> `whatsNew`
- `描述`, `Description` -> `description`
- `副标题`, `Subtitle` -> `subtitle`
- `名称`, `Name` -> `name`
- `营销链接`, `Marketing URL` -> `marketingUrl`
- `支持链接`, `Support URL` -> `supportUrl`
- `隐私政策链接`, `Privacy Policy URL` -> `privacyPolicyUrl`
- `隐私选项链接`, `Privacy Choices URL` -> `privacyChoicesUrl`
- `隐私政策文本`, `Privacy Policy Text` -> `privacyPolicyText`

If the Markdown omits the resource type, infer it only when the fields clearly belong to one ASC resource according to OpenAPI. For example, `promotionalText`, `keywords`, and `whatsNew` point to `appStoreVersionLocalizations` in this bundled spec. If multiple resources are plausible, ask the user to confirm.

If the Markdown omits the resource id needed by a mutating endpoint, first try to discover it through ASC API when the user asked to operate on the current project or a named app. Do not guess ids from app names without API evidence. If discovery cannot identify exactly one target, stop and ask the user to choose or provide the id.

## Resolving Missing ASC IDs

Use user-provided identifiers when present:

- `Resource`
- ASC resource `ID`
- bundle id
- app name
- version string
- platform
- locale
- screenshot set id

When these details are missing, discover them instead of forcing the user to manually browse App Store Connect.

For the current local project, inspect project files read-only to find likely app identity:

- Xcode project settings, `Info.plist`, build settings, entitlements, or `.xcodeproj` files for bundle id and app name.
- App metadata files, localization files, README, release notes, or existing App Store docs for version, locale, and platform hints.
- Exported screenshot folders or filenames for locale, platform, and display type hints.

Then query ASC read-only to resolve real resource ids. Common discovery chain:

1. `GET /v1/apps` filtered by bundle id, app name, or SKU when available.
2. `GET /v1/apps/{appId}/appStoreVersions` filtered by platform, version string, state, or latest suitable version.
3. `GET /v1/appStoreVersions/{versionId}/appStoreVersionLocalizations` to find localization ids by locale.
4. `GET /v1/apps/{appId}/appInfos` and related `appInfoLocalizations` when fields belong to app info metadata.
5. Screenshot uploads: locate or create the correct `appScreenshotSets` using version localization, screenshot display type, locale, and platform evidence before creating `appScreenshots`. Determine `screenshotDisplayType` from the actual PNG pixel dimensions — do not guess from device name alone:

   | Dimensions (portrait) | `screenshotDisplayType` | Common devices |
   |---|---|---|
   | 1320×2868 | `APP_IPHONE_69` | iPhone 16 Pro Max |
   | 1206×2622 | `APP_IPHONE_67` | iPhone 16 Pro |
   | 1290×2796 | `APP_IPHONE_67` | iPhone 15 Pro Max, 15 Plus |
   | 1284×2778 | `APP_IPHONE_65` | iPhone 12–14 Pro Max |
   | 1242×2688 | `APP_IPHONE_65` | iPhone XS Max |
   | 1179×2556 | `APP_IPHONE_61` | iPhone 15 |
   | 1170×2532 | `APP_IPHONE_61` | iPhone 12–14 |
   | 1125×2436 | `APP_IPHONE_58` | iPhone X, XS |
   | 1080×1920 | `APP_IPHONE_55` | iPhone 6s–8 Plus |
   | 750×1334  | `APP_IPHONE_47` | iPhone 6s–8 |

   If the PNG dimensions do not match any row above, check Apple's current screenshot specifications before assigning a display type. Never assume a display type from a device marketing name such as "iPhone 17 Pro" without verifying the actual exported pixel dimensions.

After discovery, summarize the matched target before generating mutating JSON:

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

If multiple ASC resources match, list the candidates and ask the user to choose. If no resource matches, explain the missing evidence and ask for the smallest needed identifier, usually bundle id, version, locale, or resource id.

Before executing any `POST`, `PATCH`, or `DELETE`, output the generated standard task JSON for user confirmation and stop. Markdown is allowed to be flexible; the final JSON is not. Only continue to upload or modify App Store Connect after the user explicitly confirms the shown JSON.

Generated task JSON shape:

The output is always a JSON **array**. Each locale and each independent resource produces one item. Never collapse multiple locales into a single object or produce a content summary.

```json
[
  {
    "method": "PATCH",
    "path": "/v1/appStoreVersionLocalizations/{real-id-from-discovery}",
    "body": {
      "data": {
        "type": "appStoreVersionLocalizations",
        "id": "{real-id-from-discovery}",
        "attributes": {
          "promotionalText": "更安静地记录每一天。",
          "keywords": "日记,情绪,照片,记录,生活",
          "whatsNew": "- 优化了记录体验\n- 修复了一些细节问题"
        }
      }
    }
  },
  {
    "method": "PATCH",
    "path": "/v1/appStoreVersionLocalizations/{real-id-from-discovery}",
    "body": {
      "data": {
        "type": "appStoreVersionLocalizations",
        "id": "{real-id-from-discovery}",
        "attributes": {
          "promotionalText": "Quietly capture every day.",
          "keywords": "journal,mood,photo,log,life",
          "whatsNew": "- Improved recording experience\n- Fixed minor issues"
        }
      }
    }
  }
]
```

IDs in the `path` and `data.id` fields must come from real ASC API discovery. Never invent or reuse placeholder IDs. A content summary object such as `{"app": {...}, "locales": [...]}` is not a valid task JSON output and must never be generated.

When the user provides multiple Markdown files or multiple sections, convert each independent target resource into one task JSON item. Summarize all tasks and ask for one confirmation before execution.

## Workflow

1. Classify the request.
   - Read-only: list, inspect, fetch, summarize, export.
   - Mutating: create, patch, delete, submit, upload, link, assign, change state.

2. Find the endpoint from OpenAPI.
   - If the user provided Markdown update content, first extract resource, resource id, locale hints, and candidate attributes.
   - If resource ids or app identity are missing, inspect the current local project read-only and query ASC read-only to resolve the exact target.
   - Search by user wording, resource name, or path.
   - Inspect method, parameters, required body schema, relationships, and response shape.
   - Prefer official ASC resource names from the spec.
   - Generate the JSON skeleton with `inspect_openapi.py template METHOD /path` before drafting payload files for `POST` or `PATCH`.
   - Validate extracted Markdown fields against the OpenAPI-generated attributes. Drop or question fields that the schema does not allow.

3. Draft a minimal local script or command.
   - Reuse `scripts/asc_client.py` where possible.
   - Keep generated scripts project-local and credential-free.
   - Do not duplicate the full OpenAPI spec into generated code.

4. Execute safely only when appropriate.
   - For `GET`, run the script if the user asked for live data and local network access is available/approved.
   - For `POST`, `PATCH`, or `DELETE`, show the generated standard task JSON first, including method, endpoint, resource id, and body, then stop. Ask for confirmation before running. Do not upload or modify ASC in the same turn that first creates the final JSON unless the user already explicitly approved that exact JSON.
   - If the caller provided an output path (for example, as a subagent receiving `output path: /some/path/asc-tasks.json`), write the final task JSON to that exact path before stopping for confirmation. Confirm the absolute path in the completion summary so the caller can locate it. If no output path was provided, print the JSON in the current conversation only.

5. Report results.
   - Summarize ASC response data in human-readable form.
   - Include status codes and response bodies for errors.
   - For auth/signing errors, instruct the user to check `~/.asc_secrets` locally and remind them that Codex has no permission to read their secrets.
   - Do not include request headers, JWTs, `.p8` paths beyond the configured path string, or secret file contents.

## Python Client Pattern

Prefer importing from `scripts/asc_client.py`:

```python
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent / "asc-api" / "scripts"))
from asc_client import ASCClient

client = ASCClient()
data = client.get("/v1/apps", params={"limit": 20})
for app in data.get("data", []):
    attrs = app.get("attributes", {})
    print(attrs.get("name"), attrs.get("bundleId"))
```

For one-off scripts inside another project, copy the safe pattern but keep `~/.asc_secrets` and `.p8` outside the project.

## Output Quality Bar

A good ASC automation answer:

- Uses the bundled OpenAPI spec to choose the endpoint and schema.
- Keeps code small and obvious.
- Separates read-only and mutating operations.
- States exactly what will be sent to Apple for mutating calls.
- Never exposes credentials, JWTs, or Authorization headers.
- Leaves the user with runnable local code or verified live results.
