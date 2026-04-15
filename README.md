# czm

`czm` is a production CLI client for the eczema treatment tracker backend.

It talks to the real API over HTTP, uses API-key auth only, and follows the backend contract for subjects, locations, episodes, applications, due items, and events.

## Quick Start

1. Follow the full getting-started tutorial: [docs/getting-started.md](docs/getting-started.md)
2. Read the command reference for the full command-by-command manual: [docs/reference.md](docs/reference.md)
3. Read the implementation notes below if you want the non-obvious behavior explained.

## Agent Skill

This repository now includes an Agent Skills-compatible skill package at [`skills/czm`](skills/czm). It is procedural guidance for agents that need to use `czm` to manage eczema episodes, check what is due, and log treatment applications.

Suggested use:

1. Read [skills/czm/SKILL.md](skills/czm/SKILL.md) first. In an Agent Skills-compatible runtime, this file is the entry point that the agent loader reads to decide when the skill applies and what to do next.
2. Read the reference files under [`skills/czm/references`](skills/czm/references) for exact workflows, commands, and error handling.
3. Use `czm setup` first, then `czm due list`, `czm episode get`, `czm episode heal`, `czm episode relapse`, and `czm application log` as needed.

How loading works:

- `SKILL.md` is plain markdown with YAML frontmatter.
- The agent runtime indexes that file, looks at the `name` and `description`, and matches it to the user request.
- If the skill matches, the runtime reads the routing rules in `SKILL.md` and then the referenced files for details.
- Nothing in `skills/czm` is executed by the CLI itself; it is guidance for an agent that knows how to consume Agent Skills.

What the user has to do:

- Usually nothing inside `czm` itself.
- The skill must be available to the OpenClaw or Agent Skills runtime as files on disk, either by checking out this repository where the runtime can read it or by copying/symlinking `skills/czm` into the runtime's configured skill directory.
- If OpenClaw runs as a different Unix user, that user must also be able to read the skill files.
- Once the runtime can see the skill, requests about eczema tracking are routed to this skill automatically.

Installer helper:

If you want a one-command install from this repository clone into a skill directory you control, run:

```bash
python3 scripts/install_skill.py --target-dir /path/to/openclaw/skills
```

That command copies `skills/czm` into `/path/to/openclaw/skills/czm`. If you prefer a symlink instead of a copy, add `--mode symlink`.

More detail: [docs/skill-install.md](docs/skill-install.md)

Layout:

- [`skills/czm/SKILL.md`](skills/czm/SKILL.md)
- [`skills/czm/references/commands.md`](skills/czm/references/commands.md)
- [`skills/czm/references/workflows.md`](skills/czm/references/workflows.md)
- [`skills/czm/references/entity-resolution.md`](skills/czm/references/entity-resolution.md)
- [`skills/czm/references/error-handling.md`](skills/czm/references/error-handling.md)
- [`skills/czm/references/examples.md`](skills/czm/references/examples.md)
- [`skills/czm/references/protocol.md`](skills/czm/references/protocol.md)

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
