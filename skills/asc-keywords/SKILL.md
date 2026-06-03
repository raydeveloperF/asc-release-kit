---
name: asc-keywords
description: Generate localized ASC keyword-field recommendations for iOS apps. Use when the user asks for App Store Connect keywords, ASO keyword research, localized ASC keyword sets, or a 100-character keyword field. Focus only on the hidden Keywords field, not title, subtitle, screenshots, descriptions, or other ASC metadata.
---

# ASC Keywords

Use this skill to produce one or more localized App Store Connect `Keywords` fields. The deliverable is keyword-only ASO output: no subtitle, no title rewrite, no screenshot copy, no marketing description.

## Project Context First

Before keyword research, gather enough context to understand the current app. Do not jump straight from a category label to final keywords.

If a local project or workspace is available, inspect the relevant app files first, such as product docs, README, app entry points, feature screens, localization files, existing App Store metadata, or marketing copy. Keep the pass lightweight and read-only unless the user asks for edits.

Build a short working brief before generating candidates:

- App name, category, and target platforms.
- Core user job and the 3-5 strongest implemented features.
- Target audience, usage scenario, and likely search intent.
- Existing title/subtitle/metadata words that must not be duplicated in `Keywords`.
- Localization languages and any locale-specific product differences.
- Competitive posture: new indie app, niche app, or already established app.

If the project context is missing or too thin, ask focused questions or request the minimum files/evidence needed. It is acceptable to produce a starter keyword set only after labeling it as context-limited and pending App Store validation.

## Required Inputs

Ask for missing essentials before producing final keyword strings:

- Target localization languages/locales, such as `en-US`, `zh-Hans`, `ja`, or `de-DE`.
- App category and core user job.
- 3-8 seed function words per locale, preferably in the target language.

Useful optional inputs:

- App name and existing title/subtitle, only to avoid duplicate words in the keyword field.
- Top competitors per locale.
- Manual App Store autocomplete phrases, competitor titles/subtitles, and user review/pain-point phrases.
- Whether the app is new/indie or already has strong ranking/install volume.

If the user only gives languages and a rough app idea, create a starter set and clearly label it as "needs App Store manual validation".

## Source Capture Workflow

Prefer user-provided App Store evidence over generic web guesses.

1. Collect official-intent candidates.
   - Ask the user to type core function words into the App Store search box on iPhone for each locale and paste the autocomplete suggestions.
   - Treat autocomplete phrases as high-signal because they reflect real App Store search intent.

2. Extract competitor vocabulary.
   - Ask for the top 3 direct competitors per locale.
   - Pull industry/function words from competitor app names and visible metadata if available.
   - Keep generic industry words; do not copy trademarked brand names unless the user explicitly wants a legal-risk review.

3. Add user-language candidates.
   - Include synonyms for core functions in the target language.
   - Include short pain-point words from real reviews, support tickets, or user interviews.
   - Prefer words users search for, not internal product terminology.

## Saturation Screening

For each candidate or autocomplete phrase, classify the competitive shape:

- `avoid`: top results are dominated by large brands, platform giants, or exact-brand intent.
- `keep`: results include small or indie apps, lower-review apps, or mixed-quality competitors.
- `priority`: a relevant long-tail phrase has weak-looking competition and direct product fit.
- `unclear`: insufficient evidence; keep only if it is semantically strong and space-efficient.

Bias toward long-tail component words that can combine into multiple useful phrases. For a new indie app, do not spend scarce characters on giant head terms unless they are short, essential, and highly reusable.

## Keyword Field Rules

Build each localized App Store Connect keyword field under the 100-character limit.

- Use comma-separated tokens with no spaces: `word1,word2,word3`.
- Count physical characters, including commas. Keep each final string at `<= 100`.
- Do not repeat tokens already present in the provided app name/title/subtitle.
- Do not repeat tokens inside the keyword field.
- Split English phrases into component words when that saves space, such as `home,workout` rather than `home workout`.
- Remove filler and platform words: `app`, `free`, `iphone`, `ipad`, `ios`, `apple`.
- Avoid English plural duplicates when the singular is enough.
- Avoid competitor brand names, celebrity names, and trademarked terms unless explicitly requested.
- For languages without spaces, such as Chinese or Japanese, use natural searchable words/short phrases as tokens; do not force single-character splitting.
- Preserve meaningful accents or locale-specific spelling when users search that way.

## Output Format

Return a compact table per locale:

| Locale | Keywords | Count | Notes |
| --- | --- | ---: | --- |
| en-US | `journal,diary,mood,habit,photo,calendar` | 40 | starter set; validate autocomplete |

Then include:

- `Priority phrases`: 5-10 phrase combinations the token set is intended to cover.
- `Removed`: duplicates, giant-brand terms, filler/platform words, and weak terms.
- `Manual validation checklist`: exact App Store searches the user should run before shipping.

If final evidence is weak, say so plainly. Do not pretend the set is production-grade when it was built without App Store autocomplete or competitor-result checks.

## Quality Bar

A good final answer:

- Produces a ready-to-paste keyword string for every requested locale.
- Stays under 100 characters per locale.
- Explains tradeoffs briefly.
- Uses locale-native search language.
- Avoids title/subtitle recommendations unless the user separately asks for them.
- Writes the final Markdown output, grouped by language, to a file: use the output path provided by the caller if one was given, otherwise write to `asc-keywords.md` in the current working directory. Confirm the absolute path in the completion summary.
