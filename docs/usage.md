# Usage

This walkthrough uses the live backend from `http://localhost:8000` and an API key stored in configuration.

## 1. Create a subject

```bash
czm subject create --display-name "Child A" --json
```

Example output:

```json
{"id":1,"account_id":1,"display_name":"Child A","created_at":"2026-04-15T14:03:29.017819Z","updated_at":"2026-04-15T14:03:29.017822Z"}
```

## 2. Create a location

```bash
czm location create --code left_elbow --display-name "Left elbow" --json
```

Example output:

```json
{"location":{"id":1,"code":"left_elbow","display_name":"Left elbow","created_at":"2026-04-15T14:03:36.040171Z"}}
```

## 3. Create an episode

```bash
czm episode create --subject "child a" --location left --json
```

The CLI resolves `child a` against subjects and `left` against locations.

Example output:

```json
{"episode":{"id":1,"subject_id":1,"location_id":1,"status":"active_flare","current_phase_number":1,"phase_started_at":"2026-04-15T14:04:00.335546Z","phase_due_end_at":null,"protocol_version":"v1","healed_at":null,"obsolete_at":null,"created_at":"2026-04-15T14:04:00.340770Z","updated_at":"2026-04-15T14:04:00.340775Z"}}
```

## 4. List and get the episode

```bash
czm episode list
czm episode get 1
```

Example output for `get`:

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

## 5. Log an application

```bash
czm --timezone Europe/Berlin application log \
  --episode 1 \
  --applied-at 2026-04-15T20:30:00 \
  --treatment-type steroid \
  --treatment-name "Hydrocortisone 1%" \
  --quantity-text "thin layer" \
  --notes "evening dose" \
  --json
```

Example output:

```json
{"application":{"id":1,"episode_id":1,"applied_at":"2026-04-15T18:30:00Z","treatment_type":"steroid","treatment_name":"Hydrocortisone 1%","quantity_text":"thin layer","phase_number_snapshot":2,"is_voided":false,"voided_at":null,"is_deleted":false,"deleted_at":null,"notes":"evening dose","created_at":"2026-04-15T14:04:41.906219Z"}}
```

## 6. List applications

```bash
czm application list --episode 1
```

Example output:

```text
Applications:
- 1: 2026-04-15 18:30:00+00:00 steroid (phase 2)
```

## 7. Heal the episode

```bash
czm --timezone Europe/Berlin episode heal 1 --healed-at 2026-04-15T18:00:00 --json
```

The CLI converts the naive local timestamp to UTC before sending it to the backend.

Example output:

```json
{"episode":{"id":1,"subject_id":1,"location_id":1,"status":"in_taper","current_phase_number":2,"phase_started_at":"2026-04-15T16:00:00Z","phase_due_end_at":"2026-05-13T16:00:00Z","protocol_version":"v1","healed_at":"2026-04-15T16:00:00Z","obsolete_at":null,"created_at":"2026-04-15T14:04:00.340770Z","updated_at":"2026-04-15T16:00:00Z"}}
```

## 8. Relapse the episode

```bash
czm --timezone Europe/Berlin episode relapse 1 --reported-at 2026-04-15T21:00:00 --reason symptoms_returned --json
```

Example output:

```json
{"episode":{"id":1,"subject_id":1,"location_id":1,"status":"active_flare","current_phase_number":1,"phase_started_at":"2026-04-15T19:00:00Z","phase_due_end_at":null,"protocol_version":"v1","healed_at":"2026-04-15T16:00:00Z","obsolete_at":null,"created_at":"2026-04-15T14:04:00.340770Z","updated_at":"2026-04-15T19:00:00Z"}}
```

## 9. View events

```bash
czm events list --episode 1
```

Example output:

```text
Events:
- 1: 2026-04-15 14:04:00.335546+00:00 episode_created (agent)
- 7: 2026-04-15 14:05:10.269285+00:00 application_updated (agent)
- 8: 2026-04-15 14:05:14.749665+00:00 application_deleted (agent)
- 2: 2026-04-15 16:00:00+00:00 healed_marked (agent)
- 3: 2026-04-15 16:00:00+00:00 phase_entered (agent)
- 4: 2026-04-15 18:30:00+00:00 application_logged (agent)
- 5: 2026-04-15 19:00:00+00:00 relapse_marked (agent)
- 6: 2026-04-15 19:00:00+00:00 phase_entered (agent)
```

## 10. View due items

```bash
czm due list
```

Example output:

```text
Due items:
- episode 1: phase 1, due_today=True, next_due=2026-04-15 00:00:00+00:00
```

## 11. Ambiguity example

If multiple subjects match the same reference, the CLI exits with code `4`:

```bash
czm subject get "Child A"
```

Example failure:

```text
reference 'Child A' is ambiguous
```
