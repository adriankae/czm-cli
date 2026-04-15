# czm

`czm` is a production CLI client for the eczema treatment tracker backend.

It talks to the real API over HTTP, uses API-key auth only, and follows the backend contract for subjects, locations, episodes, applications, due items, and events.

## Quick Start

1. Follow the full getting-started tutorial: [docs/getting-started.md](docs/getting-started.md)
2. Read the implementation notes below if you want the non-obvious behavior explained.

## Commands

- `czm setup`
- `czm subject create`
- `czm subject list`
- `czm subject get`
- `czm location create`
- `czm location list`
- `czm episode create`
- `czm episode list`
- `czm episode get`
- `czm episode heal`
- `czm episode relapse`
- `czm application log`
- `czm application update`
- `czm application delete`
- `czm application list`
- `czm due list`
- `czm events list`

## Implementation Notes

- Config precedence is `CLI flag > environment variable > config file`.
- The config file lives at the XDG path `~/.config/czm/config.toml` by default, or the matching `XDG_CONFIG_HOME` path when that variable is set.
- The CLI uses `X-API-Key` for authentication.
- Subject resolution is deterministic: exact match, then case-insensitive match, then substring match.
- Location resolution follows the same rule set, checking both `code` and `display_name`.
- Naive local timestamps are interpreted in the configured CLI timezone and converted to UTC before being sent to the backend.
- JSON mode prints the backend-shaped payloads directly so the output stays strict and predictable.
- Exit codes are deterministic:
  - `0` success
  - `2` invalid request/config
  - `3` not found
  - `4` ambiguous reference
  - `5` auth failure
  - `6` conflict
  - `7` transport/server failure

## Development

Run the tests:

```bash
python3 -m pytest
```

Install editable:

```bash
PIP_INDEX_URL=https://pypi.org/simple python3 -m pip install -e .
```
