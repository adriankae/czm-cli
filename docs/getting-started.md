# Getting Started

This guide takes you from a fresh install to your first working `czm` commands.

## 1. Install the CLI

If you have not installed the package yet, do that first:

```bash
python3 -m venv .venv
source .venv/bin/activate
PIP_INDEX_URL=https://pypi.org/simple python3 -m pip install -e .
```

If the `czm` command is not found, add your virtual environment or user bin directory to `PATH`. On macOS user-site installs, that is often something like `~/Library/Python/3.13/bin`.

## 2. Start the backend

Open a second terminal, change into the backend repository, and start the Docker stack:

```bash
cd /path/to/Eczema-Tracker
docker compose up -d --build
```

Wait until the API is ready:

```bash
curl -sS http://localhost:8000/health
```

You should see:

```json
{"status":"ok"}
```

## 3. Log in to the backend

The backend seeds a default account on first startup:

- username: `admin`
- password: `admin`

Use it to get a bearer token:

```bash
ACCESS_TOKEN=$(
  curl -sS -X POST http://localhost:8000/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])'
)
```

If you prefer, you can paste the JSON response into a shell variable manually instead.

## 4. Create an API key

`czm` uses API-key auth, not the bearer token directly.

Create a dedicated key for the CLI:

```bash
curl -sS -X POST http://localhost:8000/api-keys \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"czm-cli"}'
```

The response includes a `plaintext_key`. That exact value is what you put into `czm` config.

Example response shape:

```json
{
  "api_key": {
    "id": 1,
    "account_id": 1,
    "name": "czm-cli",
    "is_active": true,
    "created_at": "2026-04-15T14:02:57.724857Z",
    "last_used_at": null
  },
  "plaintext_key": "paste-this-value-into-czm"
}
```

## 5. Configure `czm`

Create the config file at `~/.config/czm/config.toml` or `$XDG_CONFIG_HOME/czm/config.toml`:

```toml
base_url = "http://localhost:8000"
api_key = "paste-this-value-into-czm"
timezone = "Europe/Berlin"
```

If you do not want a config file yet, you can pass `--base-url` and `--api-key` on every command.

## 6. Run your first command

Start with the simplest read-only command:

```bash
czm subject list
```

If the backend only has the default `admin` account and no subjects yet, you should see:

```text
No subjects.
```

## 7. Create your first subject and location

```bash
czm subject create --display-name "Child A"
czm location create --code left_elbow --display-name "Left elbow"
```

You can list them to confirm:

```bash
czm subject list
czm location list
```

## 8. Create an episode

The easiest first episode uses the exact names you just created:

```bash
czm episode create --subject "Child A" --location "Left elbow"
```

If you later create more subjects or locations with similar names, the CLI will resolve them in this order:

1. exact match
2. case-insensitive match
3. substring match

If more than one item matches at the same step, the CLI stops with an ambiguity error instead of guessing.

## 9. Heal, log, and inspect

Once you have an episode, try the rest of the core workflow:

```bash
czm episode heal 1
czm application log --episode 1 --treatment-type steroid --treatment-name "Hydrocortisone 1%" --quantity-text "thin layer" --notes "morning dose"
czm application list --episode 1
czm due list
czm events list --episode 1
```

If you want machine-readable output, add `--json`.

## 10. What to do if a command fails

- `missing required configuration`: set `base_url` and `api_key`
- `unauthorized`: check that you used the plaintext API key, not the bearer token
- `reference '...' is ambiguous`: use a fuller name or the numeric ID
- `transport_error`: confirm the backend is still running on `http://localhost:8000`

