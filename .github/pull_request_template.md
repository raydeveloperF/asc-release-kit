## Summary

<!-- What does this PR change and why? 1-3 bullet points. -->

-
-

## Affected skill(s) or component(s)

<!-- Which of the following does this touch? -->

- [ ] asc-launch-workflow
- [ ] asc-metadata
- [ ] asc-keywords
- [ ] asc-screenshots
- [ ] asc-api
- [ ] pixelmator-pxd-editor
- [ ] scripts (download_openapi / validate)
- [ ] CI / GitHub Actions
- [ ] Documentation only

## Testing

<!-- Describe how you verified the change works. -->

-

## Checklist

- [ ] `python3 scripts/validate.py` passes locally
- [ ] Python files pass `python3 -m py_compile`
- [ ] No ASC credentials, `.p8` contents, JWTs, or Authorization headers are included anywhere in this PR
- [ ] `openapi.oas.json` is **not** committed (it is in `.gitignore`)
- [ ] SKILL.md frontmatter `name` matches the skill directory name (if a skill was added or renamed)
- [ ] AGENTS.md Structure section is updated (if a file or directory was added or removed)
- [ ] CHANGELOG.md has an entry under `[Unreleased]`
