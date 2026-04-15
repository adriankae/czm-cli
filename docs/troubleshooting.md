# Troubleshooting

## Backend not reachable

Symptoms:

- `transport_error`
- connection refused
- timeout

Fixes:

- confirm Docker is running
- confirm the backend stack was started with `docker compose up -d --build`
- verify `http://localhost:8000/health`
- check `base_url` in config or flags

## Invalid API key

Symptoms:

- `unauthorized`
- `invalid api key`

Fixes:

- confirm the backend was started with the seeded `admin` account
- generate a fresh API key with the backend `POST /api-keys` endpoint
- make sure `CZM_API_KEY` or the config file contains the plaintext API key, not the bearer token

## Config missing

Symptoms:

- `missing required configuration`

Fixes:

- set `CZM_BASE_URL` and `CZM_API_KEY`
- or put them in `~/.config/czm/config.toml`
- or set `XDG_CONFIG_HOME` and write the config under `$XDG_CONFIG_HOME/czm/config.toml`

## Ambiguity errors

Symptoms:

- `reference '...' is ambiguous`

Fixes:

- use a more specific subject or location reference
- prefer the exact display name or exact code
- use the numeric ID when you already know it

## Timezone issues

Symptoms:

- timestamps appear shifted by a few hours
- due calculations do not match the day you expected

Fixes:

- set `timezone` to the local timezone you actually use
- pass naive local timestamps like `2026-04-15T18:00:00`
- remember that JSON output is always UTC

