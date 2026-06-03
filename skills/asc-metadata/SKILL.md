---
name: asc-metadata
description: Write localized ASC metadata for iOS apps, including subtitle, promotional text, and app description. Use when the user asks for App Store Connect listing copy, ASC metadata, localized subtitle, promotional text, or app description. This skill requires project understanding first, and must ask for missing target languages or writing style before producing final copy.
---

# ASC Metadata

Use this skill to write localized App Store Connect copy for these fields only:

- `Subtitle`
- `Promotional Text`
- `App Description`

Do not generate keywords, screenshot headlines, release notes, privacy copy, or pricing copy unless the user separately asks for them.

## Required Inputs

Before writing final copy, check whether the user already provided both:

- Target localization languages/locales, such as `zh-Hans`, `en-US`, `ja`, or `de-DE`.
- Writing style.

If target languages are missing, stop and ask the user to provide them. Do not guess languages from the project.

If writing style is missing, stop and ask the user to provide it. Tell the user that the default style is `平静内敛`; if they choose the default, write in that style.

Ask only for the missing item or items. Keep the question short.

## Project Context First

Before writing specific metadata, gather enough context to understand the app. If a local project or workspace is available, inspect relevant files read-only unless the user asks for edits:

- README, product docs, planning docs, marketing copy, or existing App Store metadata.
- App entry points, main screens, feature modules, localization files, and screenshots if available.
- Existing title, subtitle, keywords, screenshots, and product positioning, if present.

Build a short working brief before drafting:

- App name, platform, category, and target audience.
- Core user job and the 3-5 strongest implemented features.
- Main emotional promise or practical value.
- Constraints from existing brand voice, screenshots, title, or keywords.
- Locale-specific wording risks, cultural fit, and product differences.

If the available project context is too thin, ask focused follow-up questions or label the output as a context-limited draft. Do not invent unsupported features, claims, awards, integrations, subscription terms, privacy guarantees, or medical/legal/financial promises.

## Field Rules

Use current App Store Connect limits unless the user provides different constraints:

- Subtitle: at most 30 characters.
- Promotional Text: at most 170 characters.
- App Description: at most 4000 characters, plain text, line breaks allowed, no HTML.

For every locale:

- Write in the target language, not merely translated English.
- Preserve the requested writing style.
- Keep claims grounded in the inspected project.
- Avoid duplicate wording between subtitle and the first line of the description when possible.
- Prefer concrete value over generic praise.
- Avoid filler like "best", "ultimate", "revolutionary", and unsupported superlatives.
- Do not mention Apple, iPhone, iOS, App Store, or platform terms as selling points unless directly relevant and allowed.

## Default Style: 平静内敛

When the user chooses the default style, use calm, restrained product language:

- Clear, precise, and low-pressure.
- Warm but not sentimental.
- Confident without hype.
- Short sentences, concrete nouns, few exclamation marks.
- Let the app's actual behavior carry the persuasion.

## Drafting Workflow

1. Confirm required inputs.
   - If localization languages or writing style are missing, ask and stop.

2. Understand the project.
   - Inspect project evidence first when available.
   - Summarize the working brief in 3-6 bullets before final copy.

3. Draft per locale.
   - Produce all three fields for every requested locale.
   - Fit each field within its limit.
   - Adapt wording culturally instead of doing literal translation.

4. Self-check.
   - Count characters for subtitle and promotional text.
   - Check the description is under 4000 characters.
   - Check each claim against project evidence.
   - Flag any assumption or weak evidence.

## Output Format

Start with a compact project brief:

```markdown
**Project Brief**
- App:
- Audience:
- Core value:
- Strongest features:
- Style:
```

Then provide one section per locale:

```markdown
## zh-Hans

| Field | Copy | Count |
| --- | --- | ---: |
| Subtitle | `...` | 12/30 |
| Promotional Text | `...` | 86/170 |

**App Description**

...

Count: 620/4000
```

End with:

- `Assumptions`: only if anything was inferred.
- `Evidence checked`: the files, screens, docs, or user-provided facts used.
- `Manual review`: locale or App Store Connect checks the user should run before shipping.

## Quality Bar

A good result:

- Provides subtitle, promotional text, and app description for every requested language.
- Respects all character limits.
- Sounds native in each locale.
- Matches the requested style, especially `平静内敛` when selected.
- Is grounded in the real project rather than a generic app category.
- Is ready to paste into App Store Connect after human locale review.

Finally, write the complete Markdown output, grouped by language, to a file:

- If the caller provided an output path (for example, as a subagent receiving `output path: /some/path/asc-metadata.md`), write to that exact path.
- If no output path was provided, write to `asc-metadata.md` in the current working directory.

After writing, confirm the absolute path of the written file in your completion summary so the caller can locate it.
