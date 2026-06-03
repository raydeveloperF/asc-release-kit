#!/usr/bin/env python3
"""Safe local App Store Connect API client.

Reads credentials from ~/.asc_secrets, signs a short-lived JWT in local memory,
and sends requests directly to Apple's REST API. Do not print tokens or headers.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any


BASE_URL = "https://api.appstoreconnect.apple.com"
SECRET_KEYS = ("ASC_KEY_ID", "ASC_ISSUER_ID", "ASC_KEY_PATH")
SECRET_CHECK_HINT = (
    "Check ~/.asc_secrets and the .p8 path manually on this Mac. "
    "Codex cannot and should not access your secret file, private key, JWT, "
    "or Authorization header."
)


def load_asc_secrets(path: Path | None = None) -> dict[str, str]:
    secrets_path = path or (Path.home() / ".asc_secrets")
    if not secrets_path.exists():
        raise FileNotFoundError(
            f"Missing {secrets_path}. Create it manually with ASC_KEY_ID, "
            f"ASC_ISSUER_ID, and ASC_KEY_PATH. {SECRET_CHECK_HINT}"
        )

    values: dict[str, str] = {}
    for raw_line in secrets_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in SECRET_KEYS:
            values[key] = value.strip().strip("\"'")

    missing = [key for key in SECRET_KEYS if not values.get(key)]
    if missing:
        raise ValueError(
            f"Missing required keys in {secrets_path}: {', '.join(missing)}. "
            f"{SECRET_CHECK_HINT}"
        )
    return values


def generate_jwt(secrets: dict[str, str]) -> str:
    try:
        import jwt
    except ModuleNotFoundError as error:
        raise RuntimeError("Missing dependency: run `pip3 install pyjwt cryptography`.") from error

    private_key_path = Path(os.path.expanduser(secrets["ASC_KEY_PATH"]))
    private_key = private_key_path.read_text(encoding="utf-8")
    now = int(time.time())
    payload = {
        "iss": secrets["ASC_ISSUER_ID"],
        "exp": now + 1200,
        "aud": "appstoreconnect-v1",
    }
    headers = {
        "alg": "ES256",
        "kid": secrets["ASC_KEY_ID"],
        "typ": "JWT",
    }
    return jwt.encode(payload, private_key, algorithm="ES256", headers=headers)


class ASCClient:
    def __init__(self, secrets_path: Path | None = None) -> None:
        self.secrets = load_asc_secrets(secrets_path)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            import requests
        except ModuleNotFoundError as error:
            raise RuntimeError("Missing dependency: run `pip3 install requests`.") from error

        token = generate_jwt(self.secrets)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        url = f"{BASE_URL}{path if path.startswith('/') else '/' + path}"
        response = requests.request(method.upper(), url, headers=headers, params=params, json=body)

        if not response.ok:
            raise RuntimeError(
                f"{method.upper()} {path} failed with {response.status_code}:\n"
                f"{response.text}\n"
                f"If this is an auth or permission error, {SECRET_CHECK_HINT}"
            )

        if not response.text:
            return {}
        return response.json()

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("GET", path, params=params)

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", path, body=body)

    def patch(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> dict[str, Any]:
        return self.request("DELETE", path)


def parse_pairs(items: list[str]) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected key=value, got: {item}")
        key, value = item.split("=", 1)
        pairs[key] = value
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser(description="Safe local App Store Connect API client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_apps = subparsers.add_parser("list-apps")
    list_apps.add_argument("--limit", default="20")

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("path")
    get_parser.add_argument("--query", action="append", default=[], help="Query pair: key=value")

    args = parser.parse_args()
    client = ASCClient()

    if args.command == "list-apps":
        data = client.get("/v1/apps", params={"limit": args.limit})
        for app in data.get("data", []):
            attrs = app.get("attributes", {})
            print(f"{app.get('id')} | {attrs.get('name')} | {attrs.get('bundleId')}")
        return

    if args.command == "get":
        print(json.dumps(client.get(args.path, params=parse_pairs(args.query)), indent=2))


if __name__ == "__main__":
    main()
