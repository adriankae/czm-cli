# Setup

`czm` reads configuration in this order:

1. CLI flags
2. Environment variables
3. Config file

## Config file path

The default config file is:

```text
~/.config/czm/config.toml
```

If `XDG_CONFIG_HOME` is set, the file is read from:

```text
$XDG_CONFIG_HOME/czm/config.toml
```

## Environment variables

- `CZM_BASE_URL`
- `CZM_API_KEY`
- `CZM_TIMEZONE`

## Example config

```toml
base_url = "http://localhost:8000"
api_key = "your-api-key-here"
timezone = "Europe/Berlin"
```

## What the settings mean

- `base_url` is the backend API root, for example `http://localhost:8000`
- `api_key` is the backend API key sent as `X-API-Key`
- `timezone` is the local timezone used to interpret naive timestamps before converting them to UTC

## Example CLI override

```bash
czm --base-url http://localhost:8000 --api-key "$CZM_API_KEY" subject list
```

