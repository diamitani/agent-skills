# Project board organizer

Canonical skill that audits a messy project board (Asana, ClickUp, Monday, Trello, Notion, or Jira), rewrites tasks for a chosen audience, proposes a clean section structure, and applies approved changes with a preview first.

Platform packs are generated into `dist/<platform>/project-board-organizer/` by `scripts/build.py`.

## What's new in v2

- **Health audit** before rewriting (overdue, unassigned, vague names, duplicates, empty sections)
- **Snapshot + rollback** — raw board saved before writes; can restore names, notes, and sections
- **Preserves original notes** under an `Original notes:` block instead of discarding them
- **No invented facts** — missing dates/owners stay generic and go under "Questions for the owner"
- **Partial approvals** — apply names only, skip section changes, exclude specific tasks
- **Connector-first** — prefers an installed app connector; tokens only as fallback

## Relationship to skill-asana-organizer

Upgraded from [diamitani/skill-asana-organizer](https://github.com/diamitani/skill-asana-organizer), which keeps the Claude Code `SKILL.md`, bash connectors, and MCP server.

## License

MIT © Patrick Diamitani, 2026
