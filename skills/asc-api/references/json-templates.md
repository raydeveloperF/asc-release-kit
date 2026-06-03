# App Store Connect JSON Templates

These templates are generated from `references/openapi.oas.json` with `scripts/inspect_openapi.py template`.

Regenerate before relying on them if `openapi.oas.json` changes.

## Update App Store Version Localization

Command:

```bash
python3 asc-api/scripts/inspect_openapi.py template PATCH /v1/appStoreVersionLocalizations/{id}
```

Template:

```json
{
  "method": "PATCH",
  "path": "/v1/appStoreVersionLocalizations/{id}",
  "body": {
    "data": {
      "type": "appStoreVersionLocalizations",
      "id": "RESOURCE_ID",
      "attributes": {
        "description": "",
        "keywords": "",
        "marketingUrl": "",
        "promotionalText": "",
        "supportUrl": "",
        "whatsNew": ""
      }
    }
  }
}
```

For a minimal update, keep only the attributes being changed. Example:

```json
{
  "method": "PATCH",
  "path": "/v1/appStoreVersionLocalizations/RESOURCE_ID",
  "body": {
    "data": {
      "type": "appStoreVersionLocalizations",
      "id": "RESOURCE_ID",
      "attributes": {
        "promotionalText": "",
        "keywords": ""
      }
    }
  }
}
```

## Update App Info Localization

Command:

```bash
python3 asc-api/scripts/inspect_openapi.py template PATCH /v1/appInfoLocalizations/{id}
```

Template:

```json
{
  "method": "PATCH",
  "path": "/v1/appInfoLocalizations/{id}",
  "body": {
    "data": {
      "type": "appInfoLocalizations",
      "id": "RESOURCE_ID",
      "attributes": {
        "name": "",
        "subtitle": "",
        "privacyPolicyUrl": "",
        "privacyChoicesUrl": "",
        "privacyPolicyText": ""
      }
    }
  }
}
```
