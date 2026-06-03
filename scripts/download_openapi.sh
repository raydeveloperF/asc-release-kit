#!/usr/bin/env bash
# Download the App Store Connect OpenAPI specification from Apple.
#
# The spec (openapi.oas.json, ~6 MB) is NOT committed to this repository.
# Run this script once after cloning, before using the asc-api skill.
#
# Apple releases: https://developer.apple.com/news/releases/
# Current tested version: 4.3.1 (released 2026-05-12)
# Download page: https://developer.apple.com/documentation/appstoreconnectapi

set -euo pipefail

DEST="skills/asc-api/references/openapi.oas.json"
ZIP_URL="https://developer.apple.com/sample-code/app-store-connect/app-store-connect-openapi-specification.zip"

# Run from repo root.
if [[ ! -f "AGENTS.md" ]]; then
  echo "ERROR: Run this script from the repository root." >&2
  exit 1
fi

if [[ -f "$DEST" ]]; then
  echo "openapi.oas.json already exists at $DEST"
  echo "Delete it first if you want to re-download a newer version."
  exit 0
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "Downloading App Store Connect OpenAPI spec from Apple…"
curl -fsSL "$ZIP_URL" -o "$TMP/spec.zip"

echo "Extracting…"
unzip -q "$TMP/spec.zip" -d "$TMP/extracted"

# Apple ships the spec as openapi.oas.json at the zip root.
EXTRACTED_JSON="$TMP/extracted/openapi.oas.json"
if [[ ! -f "$EXTRACTED_JSON" ]]; then
  echo "ERROR: openapi.oas.json not found inside the zip. Contents:" >&2
  ls "$TMP/extracted/" >&2
  exit 1
fi

cp "$EXTRACTED_JSON" "$DEST"
echo "Saved to $DEST"
echo ""
echo "Smoke test:"
python3 skills/asc-api/scripts/inspect_openapi.py search apps | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(f'  OK — {len(d)} endpoint(s) matched')"
