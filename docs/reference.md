# Command Reference

This page lists every `czm` command, what it does, and a working example.

All commands use the same configuration rules:

1. CLI flags
2. environment variables
3. config file at `~/.config/czm/config.toml` or `$XDG_CONFIG_HOME/czm/config.toml`

If you are just getting started, run `czm setup` first and then read [Getting Started](getting-started.md).

## `czm setup`

Create the local config file automatically by logging into the backend, creating an API key, and writing `config.toml`.

Example:

```bash
czm setup \
  --base-url http://localhost:8000 \
  --username admin \
  --password admin \
  --api-key-name czm-cli \
  --timezone Europe/Berlin
```

Output:

```text
Wrote config to ~/.config/czm/config.toml
Next: run `czm subject list`
```

## `czm subject create`

Create a tracked subject for your account.

Arguments:

- `--display-name` subject name shown in lists and resolution

Example:

```bash
czm subject create --display-name "Child A"
```

Example output:

```text
id            1
display_name  Child A
```

## `czm subject list`

List all subjects for the authenticated account.

Example:

```bash
czm subject list
```

Example output:

```text
Subjects:
- 1: Child A
- 2: Child B
```

## `czm subject get`

Get one subject by numeric ID or by resolved text reference.

Resolution order:

1. exact match
2. case-insensitive match
3. substring match

Example:

```bash
czm subject get "Child A"
```

Example output:

```text
id            1
display_name  Child A
```

## `czm location create`

Create a body location.

Arguments:

- `--code` machine-friendly unique code
- `--display-name` human-readable label

Example:

```bash
czm location create --code left_elbow --display-name "Left elbow"
```

Example output:

```text
id            1
code          left_elbow
display_name  Left elbow
```

## `czm location list`

List all locations for the authenticated account.

Example:

```bash
czm location list
```

Example output:

```text
Locations:
- 1: left_elbow (Left elbow)
```

## `czm episode create`

Create an episode for a subject at a location.

Arguments:

- `--subject` subject name or ID
- `--location` location code, display name, or ID
- `--protocol-version` protocol version, defaults to `v1`

Example:

```bash
czm episode create --subject "Child A" --location "Left elbow"
```

Example output:

```text
id                    1
subject_id            1
location_id           1
status                active_flare
current_phase_number  1
phase_started_at      2026-04-15T14:04:00.335546Z
phase_due_end_at      None
healed_at             None
obsolete_at           None
```

## `czm episode list`

List episodes, optionally filtered by subject or status.

Arguments:

- `--subject` subject reference
- `--status` episode status such as `active_flare`, `in_taper`, or `obsolete`

Example:

```bash
czm episode list --subject "Child A"
```

Example output:

```text
Episodes:
- 1: subject 1, location 1, phase 1, active_flare
```

## `czm episode get`

Get one episode by numeric ID.

Example:

```bash
czm episode get 1
```

Example output:

```text
id                    1
subject_id            1
location_id           1
status                active_flare
current_phase_number  1
phase_started_at      2026-04-15T14:04:00.335546Z
phase_due_end_at      None
healed_at             None
obsolete_at           None
```

## `czm episode heal`

Mark an active episode as healed and move it into phase 2.

Arguments:

- `episode` episode ID
- `--healed-at` optional local timestamp in the configured timezone

Example:

```bash
czm episode heal 1 --healed-at 2026-04-15T18:00:00
```

Example output:

```text
status                in_taper
current_phase_number  2
phase_started_at      2026-04-15T16:00:00Z
phase_due_end_at      2026-05-13T16:00:00Z
```

## `czm episode relapse`

Reset an episode back to phase 1 after relapse.

Arguments:

- `episode` episode ID
- `--reported-at` optional local timestamp in the configured timezone
- `--reason` human-readable relapse reason

Example:

```bash
czm episode relapse 1 --reported-at 2026-04-15T21:00:00 --reason symptoms_returned
```

Example output:

```text
status                active_flare
current_phase_number  1
phase_started_at      2026-04-15T19:00:00Z
```

## `czm application log`

Log a treatment application against an episode.

Arguments:

- `--episode` episode ID
- `--applied-at` optional local timestamp
- `--treatment-type` one of `steroid`, `emollient`, or `other`
- `--treatment-name` optional product name
- `--quantity-text` optional amount text
- `--notes` optional note

Example:

```bash
czm application log \
  --episode 1 \
  --applied-at 2026-04-15T20:30:00 \
  --treatment-type steroid \
  --treatment-name "Hydrocortisone 1%" \
  --quantity-text "thin layer" \
  --notes "evening dose"
```

Example output:

```text
id                 1
episode_id         1
applied_at         2026-04-15T18:30:00Z
treatment_type     steroid
treatment_name     Hydrocortisone 1%
quantity_text      thin layer
phase_number_snapshot  2
is_voided          False
voided_at          None
notes              evening dose
```

## `czm application update`

Edit an existing application.

Arguments:

- `application` application ID
- `--applied-at` optional local timestamp
- `--treatment-type` optional new treatment type
- `--treatment-name` optional new treatment name
- `--quantity-text` optional new amount text
- `--notes` optional replacement notes

Example:

```bash
czm application update 1 --notes "updated note"
```

Example output:

```text
id                 1
episode_id         1
notes              updated note
```

## `czm application delete`

Mark an application as deleted.

Arguments:

- `application` application ID

Example:

```bash
czm application delete 1
```

Example output:

```text
id                 1
is_deleted         True
deleted_at         2026-04-15T14:05:14.749665Z
```

## `czm application list`

List applications for an episode.

Arguments:

- `--episode` episode ID
- `--include-voided` include voided entries as well as active ones

Example:

```bash
czm application list --episode 1
```

Example output:

```text
Applications:
- 1: 2026-04-15 18:30:00+00:00 steroid (phase 2)
```

## `czm due list`

Show which episodes are due for treatment today.

Arguments:

- `--subject` optional subject reference to filter the list

Example:

```bash
czm due list
```

Example output:

```text
Due items:
- episode 1: phase 2, due_today=False, next_due=2026-04-17 00:00:00+00:00
```

## `czm events list`

List episode events in timeline order.

Arguments:

- `--episode` episode ID
- `--event-type` optional event type filter

Example:

```bash
czm events list --episode 1
```

Example output:

```text
Events:
- 1: 2026-04-15 14:04:00.335546+00:00 episode_created (agent)
- 2: 2026-04-15 16:00:00+00:00 healed_marked (agent)
- 3: 2026-04-15 16:00:00+00:00 phase_entered (agent)
```

## `czm events timeline`

Show the same event stream as a timeline view.

Example:

```bash
czm events timeline --episode 1
```

Example output:

```text
Events:
- 1: 2026-04-15 14:04:00.335546+00:00 episode_created (agent)
- 2: 2026-04-15 16:00:00+00:00 healed_marked (agent)
- 3: 2026-04-15 16:00:00+00:00 phase_entered (agent)
```

## Output modes

- Use `--json` for machine-readable output
- Use `--quiet` to suppress human output for successful commands
- Use `--no-color` for terminals that should not receive colored text

## Common troubleshooting

- If you see `missing required configuration`, run `czm setup`
- If you see `unauthorized`, make sure the config contains the plaintext API key
- If a name is ambiguous, use a more specific reference or a numeric ID

