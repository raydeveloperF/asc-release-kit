# Setting Up App Store Connect API Access

The `asc-api` skill uses the [App Store Connect REST API](https://developer.apple.com/documentation/appstoreconnectapi) with a local API key. This guide walks through generating the key, storing it safely, and verifying the setup.

---

## 1. Check Your Role

You need **Account Holder** or **Admin** role in App Store Connect to create API keys.

To check: open [App Store Connect](https://appstoreconnect.apple.com) → click your name in the top-right → **Permissions**. Your role is listed next to each app or at the top for team-wide roles.

If you only have Developer or Marketing role, ask your Account Holder to either upgrade your role or generate the key for you.

---

## 2. Generate an API Key

1. Sign in to [App Store Connect](https://appstoreconnect.apple.com).
2. Go to **Users and Access** → **Integrations** → **App Store Connect API**.
3. Click the **+** button next to *Team Keys*.
4. Enter a name (e.g. `asc-release-kit-local`) and select the **Admin** access level.

   > **Minimum required permissions:** Admin is recommended for the full workflow (metadata + screenshots). If you only need read access for discovery, Developer is sufficient.

5. Click **Generate**.
6. The new key appears in the table. Note these two values — you will need them in Step 4:
   - **Key ID** — shown in the *Key ID* column (e.g. `ABC1234567`)
   - **Issuer ID** — shown at the top of the page above the keys table (e.g. `12345678-1234-1234-1234-123456789012`)

---

## 3. Download the Private Key

Click **Download API Key** next to your new key.

> ⚠️ **You can only download the `.p8` file once.** If you close this dialog without downloading, you must revoke the key and create a new one.

The downloaded file is named `AuthKey_XXXXXXXXXX.p8` where `XXXXXXXXXX` is your Key ID.

Move it to a safe location **outside any project directory**. The recommended location:

```bash
mkdir -p ~/.ssh
mv ~/Downloads/AuthKey_XXXXXXXXXX.p8 ~/.ssh/AuthKey_XXXXXXXXXX.p8
chmod 600 ~/.ssh/AuthKey_XXXXXXXXXX.p8
```

---

## 4. Create `~/.asc_secrets`

Create the credential file in your home directory:

```bash
touch ~/.asc_secrets
chmod 600 ~/.asc_secrets
```

Open it in a text editor and add the three values from Steps 2 and 3:

```text
ASC_KEY_ID=ABC1234567
ASC_ISSUER_ID=12345678-1234-1234-1234-123456789012
ASC_KEY_PATH=/Users/YOUR_USERNAME/.ssh/AuthKey_ABC1234567.p8
```

Replace each value with your own. Use your macOS username in `ASC_KEY_PATH` (run `whoami` in Terminal if unsure).

---

## 5. Install Python Dependencies

```bash
pip install -r skills/asc-api/scripts/requirements.txt
```

Or manually:

```bash
pip3 install requests pyjwt cryptography
```

---

## 6. Download the OpenAPI Spec

The spec is not included in this repository. Run the download script once from the repo root:

```bash
bash scripts/download_openapi.sh
```

---

## 7. Verify the Setup

Run the safe list-apps command to confirm credentials and network access work:

```bash
python3 skills/asc-api/scripts/asc_client.py list-apps
```

Expected output:

```
1234567890 | My App | com.example.myapp
```

If you see an error, check the section below.

---

## Troubleshooting

### `FileNotFoundError: Missing ~/.asc_secrets`
The file does not exist or is in the wrong location. Run `ls ~/.asc_secrets` to confirm it exists.

### `Missing required keys in ~/.asc_secrets`
One or more of `ASC_KEY_ID`, `ASC_ISSUER_ID`, or `ASC_KEY_PATH` is missing or misspelled. Open `~/.asc_secrets` in a text editor and check each line.

### `FileNotFoundError` for the `.p8` file
The path in `ASC_KEY_PATH` does not match where you saved the file. Run `ls ~/.ssh/` to see the actual filename.

### `401 Unauthorized` from App Store Connect
- The key may have been revoked. Check in App Store Connect → Integrations → App Store Connect API.
- The Issuer ID may be wrong. It is shown at the top of the API keys page, not in the key row itself.
- The system clock on your Mac may be out of sync. JWTs are time-sensitive; run `date` to check.

### `403 Forbidden`
Your key does not have sufficient permissions for the requested operation. Admin access is required for metadata updates.

---

## Security Reminders

- Never paste `ASC_KEY_ID`, `ASC_ISSUER_ID`, `.p8` contents, or JWTs into a chat with any AI tool, including Claude Code or Codex.
- Never commit `~/.asc_secrets` or any `.p8` file to a repository. Both are listed in this repo's `.gitignore` as a reminder.
- If a key is compromised, revoke it immediately in App Store Connect → Integrations → App Store Connect API, then generate a new one.
