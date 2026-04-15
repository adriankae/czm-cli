# Eczema Tracker CLI Specification (v0.1)

## 0. Purpose

This document defines a **deterministic, agent-first CLI interface** for interacting with the Eczema Tracker backend (https://github.com/adriankae/Eczema-Tracker).

Design goals:

* **Agent-optimized** (primary user)
* **Strict, machine-readable contract**
* **Thin API client** (no business logic duplication)
* **Stable interface** (commands + JSON schema + exit codes)

Non-goals:

* No UI/UX optimizations for humans
* No local state beyond config/auth
* No domain logic outside backend

---

## 1. Architecture

### 1.1 High-level

```
[ Agent ]
    ↓ (CLI calls)
[ CLI (thin client) ]
    ↓ (HTTP JSON)
[ Backend API ]
    ↓
[ DB + Scheduler + State Machine ]
```

### 1.2 Principles

* CLI is a **stateless HTTP client**
* Backend is **single source of truth**
* CLI performs:

  * input normalization
  * entity resolution
  * output formatting

---

## 2. Implementation

### 2.1 Language

* Python (recommended)
* Suggested stack:

  * `typer` (CLI)
  * `httpx` (HTTP)
  * `pydantic` (schemas)
  * `rich` (optional human output)

---

## 3. Configuration

### 3.1 Precedence

```
CLI flag > ENV > config file > default
```

### 3.2 Config location (XDG)

```
~/.config/czm-cli/config.toml
```

### 3.3 Example config

```toml
base_url = "https://api.example.com"
api_key = "sk-..."
timezone = "Europe/Berlin"
```

### 3.4 Environment variables

```
CZM_BASE_URL
CZM_API_KEY
CZM_TIMEZONE
```

---

## 4. Authentication

* **API key only**
* No login command

### 4.1 Header

```
Authorization: Bearer <API_KEY>
```

---

## 5. Global CLI Behavior

### 5.1 Output modes

| Mode         | Purpose                |
| ------------ | ---------------------- |
| default      | human-readable summary |
| `--json`     | machine-readable       |
| `--quiet`    | no output on success   |
| `--no-color` | disable ANSI           |

### 5.2 Exit codes

| Code | Meaning          |
| ---- | ---------------- |
| 0    | success          |
| 1    | generic error    |
| 2    | validation error |
| 3    | not found        |
| 4    | ambiguity        |
| 5    | auth error       |
| 6    | API error        |

---

## 6. Entity Resolution

### 6.1 Supported identifiers

| Entity   | Identifiers                |
| -------- | -------------------------- |
| subject  | id, display_name           |
| location | id, code, display_name     |
| episode  | id OR (subject + location) |

### 6.2 Resolution strategy

1. Try exact match
2. Try case-insensitive match
3. Try partial match

### 6.3 Ambiguity policy

* Non-interactive (default):

  * **FAIL with structured error**
* JSON mode:

  * return candidate list

### 6.4 Ambiguity error format

```json
{
  "error": "ambiguous",
  "entity": "location",
  "candidates": [
    {"id": "loc_1", "code": "left_elbow"},
    {"id": "loc_2", "code": "left_elbow_inner"}
  ]
}
```

---

## 7. Time Handling

### 7.1 Input

* Accept:

  * ISO 8601
  * local datetime
  * date-only

### 7.2 Behavior

* Convert → UTC before API call
* Use configured timezone for parsing

### 7.3 Output

* JSON:

  * always UTC
* Human:

  * localized

---

## 8. Command Tree (v1)

```
eczema
  subject create
  subject list
  subject get

  location create
  location list

  episode create
  episode list
  episode get
  episode heal
  episode relapse

  application log
  application update
  application delete
  application list

  due list
  events list
```

---

## 9. Command Specifications

## 9.1 subject create

```bash
eczema subject create --name "Person A"
```

### JSON output

```json
{
  "id": "sub_123",
  "display_name": "Person A",
  "created_at": "2026-04-15T12:00:00Z"
}
```

---

## 9.2 location create

```bash
eczema location create --code left_elbow --name "Left Elbow"
```

---

## 9.3 episode create

```bash
eczema episode create \
  --subject "Person A" \
  --location left_elbow
```

---

## 9.4 episode heal

```bash
eczema episode heal \
  --subject "Person A" \
  --location left_elbow
```

---

## 9.5 episode relapse

```bash
eczema episode relapse \
  --subject "Person A" \
  --location left_elbow
```

---

## 9.6 application log

```bash
eczema application log \
  --subject "Person A" \
  --location left_elbow \
  --product "Steroid Cream" \
  --amount "thin layer"
```

---

## 9.7 due list

```bash
eczema due list
```

### JSON

```json
[
  {
    "episode_id": "ep_123",
    "subject": "Person A",
    "location": "left_elbow",
    "due_at": "2026-04-15T08:00:00Z"
  }
]
```

---

## 10. JSON Contract

### 10.1 Success envelope

```json
{
  "data": {...},
  "meta": {
    "request_id": "...",
    "timestamp": "..."
  }
}
```

### 10.2 Error envelope

```json
{
  "error": {
    "code": "not_found",
    "message": "...",
    "details": {}
  }
}
```

---

## 11. Agent Skill Specification (SKILL.md)

# SKILL: eczema-tracker

## Purpose

Manage eczema treatment lifecycle via CLI.

---

## Rules

1. Always use `--json`
2. Never rely on human-readable output
3. Resolve ambiguity explicitly
4. Never assume entity IDs
5. Prefer subject+location over episode_id
6. Validate before mutation

---

## Core workflows

### 1. Start episode

```
subject exists?
→ yes → create episode
→ no → create subject → create episode
```

---

### 2. Log treatment

```
find episode (subject+location)
→ log application
```

---

### 3. Mark healed

```
episode → heal
```

---

### 4. Relapse

```
episode relapse
```

---

### 5. Daily routine

```
eczema due list --json
→ iterate → log applications
```

---

## Error handling

| Error      | Action        |
| ---------- | ------------- |
| ambiguous  | ask user      |
| not_found  | create entity |
| validation | fix input     |
| auth       | stop          |

---

## 12. Command Cheat Sheet

```bash
# subjects
eczema subject create --name "Person A"
eczema subject list

# locations
eczema location create --code left_elbow

# episodes
eczema episode create --subject "Person A" --location left_elbow
eczema episode heal --subject "Person A" --location left_elbow
eczema episode relapse --subject "Person A" --location left_elbow

# applications
eczema application log --subject "Person A" --location left_elbow --product "Steroid"

# due
eczema due list --json
```

---

## 13. Query / Workflow Library

### 13.1 "What is due today?"

```
eczema due list --json
```

---

### 13.2 "Apply treatment everywhere due"

Pseudo:

```
due = get_due()
for item in due:
  eczema application log ...
```

---

### 13.3 "Create everything from scratch"

```
create subject
create location
create episode
```

---

### 13.4 "Handle relapse automatically"

```
if symptoms worsen:
  eczema episode relapse
```

---

## 14. Test Matrix

### 14.1 Required tests

* entity resolution
* ambiguity detection
* JSON schema validation
* exit codes
* timezone conversion
* API error propagation

---

## 15. Stability Guarantees

Stable:

* command names
* flags
* JSON schema
* exit codes

Unstable:

* human-readable output

---

## 16. Future Extensions (not v1)

* `doctor`
* `init`
* shell completion
* profile management
* bulk operations
* offline mode

---

# END
