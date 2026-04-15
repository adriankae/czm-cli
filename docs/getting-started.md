# Getting Started

This is the only onboarding guide you need. It covers install, backend startup, bootstrap, config creation, and the first commands that actually work.

## 1. Install `czm`

Create a virtual environment and install the CLI:

```bash
python3 -m venv .venv
source .venv/bin/activate
PIP_INDEX_URL=https://pypi.org/simple python3 -m pip install -e .
```

If `czm` is not on your `PATH`, use the binary from the virtual environment or add the user bin directory shown by `pip` to `PATH`.

## 2. Start the backend

Open the backend repository and start Docker:

```bash
cd /path/to/Eczema-Tracker
docker compose up -d --build
```

Confirm the API is alive:

```bash
curl -sS http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 3. Create the config automatically

This is the part that was missing before. Instead of manually copying a bearer token and then manually creating an API key, use `czm setup`.

The backend seeds these credentials on first start:

- username: `admin`
- password: `admin`

Run:

```bash
czm setup \
  --base-url http://localhost:8000 \
  --username admin \
  --password admin \
  --api-key-name czm-cli \
  --timezone Europe/Berlin
```

What this does:

1. logs into the backend with the username/password
2. creates an API key through the backend
3. writes `~/.config/czm/config.toml` or `$XDG_CONFIG_HOME/czm/config.toml`

Example config that gets written:

```toml
base_url = "http://localhost:8000"
api_key = "plaintext-api-key-from-the-backend"
timezone = "Europe/Berlin"
```

If your backend is running in another timezone, pass that timezone here instead. The CLI uses it to interpret naive local timestamps.

## 4. Run your first command

Now the CLI should work without extra flags:

```bash
czm subject list
```

If nothing exists yet, the output should be:

```text
No subjects.
```

## 5. Create your first subject and location

```bash
czm subject create --display-name "Child A"
czm location create --code left_elbow --display-name "Left elbow"
```

List them to confirm:

```bash
czm subject list
czm location list
```

## 6. Create an episode

Use the exact names you just created:

```bash
czm episode create --subject "Child A" --location "Left elbow"
```

The CLI resolves text references in this order:

1. exact match
2. case-insensitive match
3. substring match

If multiple items match at the same step, the CLI stops and tells you the reference is ambiguous instead of guessing.

## 7. Heal, log, and inspect

Once you have an episode, try the rest of the workflow:

```bash
czm episode heal 1
czm application log --episode 1 --treatment-type steroid --treatment-name "Hydrocortisone 1%" --quantity-text "thin layer" --notes "morning dose"
czm application list --episode 1
czm due list
czm events list --episode 1
```

Add `--json` if you want machine-readable output instead of the human format.

## 8. If something fails

- `missing required configuration`: run `czm setup`
- `unauthorized`: check that the API key came from `czm setup`, not the bearer token from login
- `reference '...' is ambiguous`: use a fuller name or the numeric ID
- `transport_error`: confirm the backend is still running on `http://localhost:8000`

## 9. What the setup command looks like under the hood

If you want to understand the manual backend flow, `czm setup` is replacing this sequence:

```bash
ACCESS_TOKEN=$(
  curl -sS -X POST http://localhost:8000/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])'
)

curl -sS -X POST http://localhost:8000/api-keys \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"czm-cli"}'
```

You no longer need to do that by hand for normal use. It is there only to show what the bootstrap step is doing for you.
