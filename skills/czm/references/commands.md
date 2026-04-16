# Commands

Use the real `czm` CLI commands below. The skill should not invent extra flags or workflows.

## Setup

`czm setup`

Purpose:

- logs into the backend
- creates a CLI API key
- writes the local config file

Common usage:

```bash
czm setup --username admin --password admin --api-key-name czm-cli
```

Default backend base URL:

```text
http://localhost:28173
```

Override if needed:

```bash
czm setup --base-url http://localhost:28173 --username admin --password admin
```

## Subjects

`czm subject create --display-name "<name>"`

`czm subject list`

`czm subject get <subject>`

Examples:

```bash
czm subject create --display-name "Child A"
czm subject list
czm subject get "Child A"
```

## Locations

`czm location create --code <code> --display-name "<label>"`

`czm location list`

Examples:

```bash
czm location create --code left_elbow --display-name "Left elbow"
czm location list
```

## Episodes

`czm episode create --subject <subject> --location <location> [--protocol-version v1]`

`czm episode list [--subject <subject>] [--status <status>]`

`czm episode get <episode>`

`czm episode heal <episode> [--healed-at <local-timestamp>]`

`czm episode relapse <episode> [--reason <text>] [--reported-at <local-timestamp>]`

Examples:

```bash
czm episode create --subject "Child A" --location "Left elbow"
czm episode heal 1 --healed-at 2026-04-15T18:00:00
czm episode relapse 1 --reason symptoms_returned --reported-at 2026-04-15T21:00:00
```

## Applications

`czm application log --episode <episode> --treatment-type <type> [--applied-at <local-timestamp>] [--treatment-name <name>] [--quantity-text <text>] [--notes <text>]`

`czm application update <application> [--applied-at <local-timestamp>] [--treatment-type <type>] [--treatment-name <name>] [--quantity-text <text>] [--notes <text>]`

`czm application delete <application>`

`czm application list --episode <episode> [--include-voided]`

Example:

```bash
czm application log --episode 1 --treatment-type steroid --treatment-name "Hydrocortisone 1%" --quantity-text "thin layer"
```

## Due and Events

`czm due list [--subject <subject>]`

`czm events list --episode <episode> [--event-type <type>]`

`czm events timeline --episode <episode>`

Examples:

```bash
czm due list
czm events list --episode 1
```

## Output Modes

- Use `--json` for machine-readable output
- Use `--quiet` to suppress human output on success
- Use `--no-color` for terminals that should not emit color

## Auth and Config

- The CLI authenticates with `X-API-Key`
- Configuration precedence is `CLI flag > environment variable > config file`
- The config file lives at `~/.config/czm/config.toml` or `$XDG_CONFIG_HOME/czm/config.toml`
