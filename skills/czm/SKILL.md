---
name: czm
description: Procedural skill for using the czm CLI to manage eczema episodes, taper guidance, due checks, and treatment logging.
---

# czm Skill

Use this skill when helping a user with eczema episode tracking through the `czm` CLI.

## Use It For

- starting or inspecting flare episodes
- checking what is due today
- marking an episode healed or relapsed
- logging treatment applications
- summarizing taper state from backend data

## Do Not Use It For

- general chat or medical advice outside the tracked workflow
- inventing backend state, IDs, or taper progress
- simulating phase progression yourself
- destructive actions without confirmation

## Operating Rules

- Prefer machine-readable output when the CLI supports it.
- Resolve subjects and locations deterministically before mutating anything.
- Never guess between ambiguous matches. Ask for clarification.
- Never assume a transition succeeded unless the CLI/backend returned success.
- Never fabricate subject, location, episode, application, or event IDs.
- Use the backend as the source of truth for due logic and progression.
- Summarize results for the user unless they explicitly ask for raw JSON.

## Workflow Guidance

- Read [commands](references/commands.md) for the exact CLI surface and output modes.
- Read [workflows](references/workflows.md) for step-by-step user flows.
- Read [entity resolution](references/entity-resolution.md) before selecting subjects or locations.
- Read [protocol](references/protocol.md) before explaining taper state or due items.
- Read [error handling](references/error-handling.md) for exit codes and recovery steps.
- Read [examples](references/examples.md) for German request mappings.

## Safety

- Ask for confirmation before deleting an application record.
- Use `czm setup` to create local configuration from backend login and API key creation.
- Do not manually advance taper phases or calculate alternate schedules.
- If the user asks what to do next, query `czm due list` and explain the backend result.

