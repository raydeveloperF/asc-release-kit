#!/usr/bin/env python3
"""Inspect the bundled App Store Connect OpenAPI spec without loading it into chat."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SPEC_PATH = Path(__file__).resolve().parents[1] / "references" / "openapi.oas.json"


def load_spec() -> dict[str, Any]:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def operation_summary(method: str, path: str, operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "method": method.upper(),
        "path": path,
        "operationId": operation.get("operationId"),
        "summary": operation.get("summary"),
        "parameters": [
            {
                "name": param.get("name"),
                "in": param.get("in"),
                "required": param.get("required", False),
                "schema": param.get("schema", {}).get("type") or param.get("schema", {}).get("$ref"),
            }
            for param in operation.get("parameters", [])
        ],
        "requestBody": bool(operation.get("requestBody")),
        "responses": list(operation.get("responses", {}).keys()),
    }


def iter_operations(spec: dict[str, Any]):
    for path, methods in spec.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() in {"get", "post", "patch", "delete"}:
                yield method, path, operation


def resolve_ref(spec: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"Only local refs are supported: {ref}")
    node: Any = spec
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def merge_all_of(spec: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
    for item in schema.get("allOf", []):
        resolved = resolve_schema(spec, item)
        merged["properties"].update(resolved.get("properties", {}))
        merged["required"].extend(resolved.get("required", []))
    for key, value in schema.items():
        if key not in {"allOf", "properties", "required"}:
            merged[key] = value
    merged["properties"].update(schema.get("properties", {}))
    merged["required"].extend(schema.get("required", []))
    merged["required"] = sorted(set(merged["required"]))
    return merged


def resolve_schema(spec: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in schema:
        return resolve_schema(spec, resolve_ref(spec, schema["$ref"]))
    if "allOf" in schema:
        return merge_all_of(spec, schema)
    return schema


def placeholder_for_schema(
    spec: dict[str, Any],
    schema: dict[str, Any],
    *,
    name: str = "",
    required_only: bool = False,
    depth: int = 0,
) -> Any:
    schema = resolve_schema(spec, schema)
    if depth > 12:
        return "..."

    if "enum" in schema:
        return schema["enum"][0] if schema["enum"] else ""

    if "const" in schema:
        return schema["const"]

    if "oneOf" in schema:
        return placeholder_for_schema(spec, schema["oneOf"][0], name=name, required_only=required_only, depth=depth + 1)

    if "anyOf" in schema:
        return placeholder_for_schema(spec, schema["anyOf"][0], name=name, required_only=required_only, depth=depth + 1)

    schema_type = schema.get("type")

    if schema_type == "object" or "properties" in schema:
        required = set(schema.get("required", []))
        output: dict[str, Any] = {}
        for key, value in schema.get("properties", {}).items():
            if required_only and key not in required:
                continue
            output[key] = placeholder_for_schema(
                spec,
                value,
                name=key,
                required_only=required_only,
                depth=depth + 1,
            )
        return output

    if schema_type == "array":
        return [
            placeholder_for_schema(
                spec,
                schema.get("items", {}),
                name=name,
                required_only=required_only,
                depth=depth + 1,
            )
        ]

    if schema_type == "integer":
        return 0

    if schema_type == "number":
        return 0.0

    if schema_type == "boolean":
        return False

    if name == "id":
        return "RESOURCE_ID"

    if name == "type":
        return "RESOURCE_TYPE"

    return ""


def request_body_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    content = operation.get("requestBody", {}).get("content", {})
    json_content = content.get("application/json") or content.get("application/vnd.api+json")
    if not json_content:
        return None
    return json_content.get("schema")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect bundled ASC OpenAPI endpoints")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("term")

    path_parser = subparsers.add_parser("path")
    path_parser.add_argument("path")

    operations_parser = subparsers.add_parser("operations")
    operations_parser.add_argument("method")
    operations_parser.add_argument("path")

    template_parser = subparsers.add_parser("template")
    template_parser.add_argument("method")
    template_parser.add_argument("path")
    template_parser.add_argument(
        "--required-only",
        action="store_true",
        help="Only include OpenAPI-required properties in the generated body",
    )

    args = parser.parse_args()
    spec = load_spec()

    if args.command == "search":
        term = args.term.lower()
        matches = []
        for method, path, operation in iter_operations(spec):
            blob = " ".join(
                str(value or "")
                for value in (path, operation.get("operationId"), operation.get("summary"))
            ).lower()
            if term in blob:
                matches.append(operation_summary(method, path, operation))
        print(json.dumps(matches[:50], indent=2))
        return

    if args.command == "path":
        methods = spec.get("paths", {}).get(args.path)
        if not methods:
            raise SystemExit(f"Path not found: {args.path}")
        summaries = [
            operation_summary(method, args.path, operation)
            for method, operation in methods.items()
            if method.lower() in {"get", "post", "patch", "delete"}
        ]
        print(json.dumps(summaries, indent=2))
        return

    if args.command == "operations":
        operation = spec.get("paths", {}).get(args.path, {}).get(args.method.lower())
        if not operation:
            raise SystemExit(f"Operation not found: {args.method.upper()} {args.path}")
        print(json.dumps(operation, indent=2))
        return

    if args.command == "template":
        operation = spec.get("paths", {}).get(args.path, {}).get(args.method.lower())
        if not operation:
            raise SystemExit(f"Operation not found: {args.method.upper()} {args.path}")

        schema = request_body_schema(operation)
        body = placeholder_for_schema(
            spec,
            schema,
            required_only=args.required_only,
        ) if schema else None
        task = {
            "method": args.method.upper(),
            "path": args.path,
            "body": body,
        }
        print(json.dumps(task, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
