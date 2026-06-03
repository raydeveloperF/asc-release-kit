#!/usr/bin/env python3
"""Validate ASC Launch Kit plugin manifests and skill files.

Usage:
    python3 scripts/validate.py            # run all checks
    python3 scripts/validate.py --json     # JSON manifests only
    python3 scripts/validate.py --skills   # SKILL.md frontmatter only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
]

REQUIRED_FRONTMATTER_KEYS = {"name", "description"}


def validate_json_manifests() -> list[str]:
    errors: list[str] = []
    for rel in MANIFESTS:
        path = ROOT / rel
        try:
            json.loads(path.read_text(encoding="utf-8"))
            print(f"  OK   {rel}")
        except FileNotFoundError:
            errors.append(f"  MISS {rel}: file not found")
        except json.JSONDecodeError as exc:
            errors.append(f"  FAIL {rel}: {exc}")
    return errors


def validate_skill_frontmatter() -> list[str]:
    errors: list[str] = []
    skill_files = sorted((ROOT / "skills").rglob("SKILL.md"))
    if not skill_files:
        errors.append("  MISS: no SKILL.md files found under skills/")
        return errors
    for path in skill_files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            errors.append(f"  FAIL {rel}: missing YAML frontmatter block (--- ... ---)")
            continue
        found = {
            line.split(":")[0].strip()
            for line in m.group(1).splitlines()
            if ":" in line
        }
        missing = REQUIRED_FRONTMATTER_KEYS - found
        if missing:
            errors.append(f"  FAIL {rel}: missing frontmatter keys: {sorted(missing)}")
        else:
            print(f"  OK   {rel}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate ASC Launch Kit repository")
    parser.add_argument("--json", dest="only_json", action="store_true",
                        help="Check JSON manifests only")
    parser.add_argument("--skills", dest="only_skills", action="store_true",
                        help="Check SKILL.md frontmatter only")
    args = parser.parse_args()

    run_all = not args.only_json and not args.only_skills
    all_errors: list[str] = []

    if run_all or args.only_json:
        print("JSON manifests:")
        all_errors += validate_json_manifests()

    if run_all or args.only_skills:
        print("SKILL.md frontmatter:")
        all_errors += validate_skill_frontmatter()

    if all_errors:
        print(f"\n{len(all_errors)} error(s):", file=sys.stderr)
        for e in all_errors:
            print(e, file=sys.stderr)
        sys.exit(1)

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
