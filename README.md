# agent-skills

Platform-agnostic **agent skills** monorepo maintained by [Patrick Diamitani](https://github.com/diamitani).

Canonical source of truth: `skills/<slug>/SKILL.md` (YAML frontmatter with `name` + `description`, then the recipe body). Optional per-skill `README.md` or `template.json`.

Generated packs live under `dist/<platform>/<slug>/` and are produced by `scripts/build.py`. Do not hand-edit `dist/`.

## Skills

| Slug | Name | Description |
|------|------|-------------|
| [project-board-organizer](skills/project-board-organizer/) | project-board-organizer | Audit and clean messy project boards (Asana, ClickUp, Monday, Trello, Notion, Jira): rewrite tasks for an audience, reorganize sections, preview before apply. |
| [social-media-cleanup](skills/social-media-cleanup/) | Social media cleanup | Audit public social content; review findings and remove approved items only. |
| [typesafe-ai](skills/typesafe-ai/) | typesafe-ai | Build typed AI judgments with evidence, thresholds, and uncertainty handling. |

## Platforms (`dist/`)

| Platform | Output | Mapping notes |
|----------|--------|---------------|
| **grokbot** | `SKILL.md` | Prefer Grok Bot / Cursor **connectors**; `/workspace` snapshots. |
| **claude** | `SKILL.md` (kebab-case `name`) | Claude Code / Agent Skills frontmatter; MCP or `skill-asana-organizer` bash connectors + env tokens. |
| **openai** | `AGENTS.md` + `instructions.md` (≤8000 chars) | Custom GPT / Agents: prefer Actions/MCP over pasting tokens. |
| **cursor** | `.mdc` rule file | Cursor rules-style frontmatter; MCP connectors first. |
| **codex** | `AGENTS.md` | Codex agent instructions; MCP or repo connector scripts. |
| **gemini** | `GEMINI.md` | Gemini extensions/tools when present; copy-ready plans if writes unavailable. |

Tool-specific lines that differ by target are appended as a **Platform notes** section (connectors vs API tokens, where snapshots live, chat-only fallbacks).

## How to add a skill

1. Create `skills/<slug>/SKILL.md` with `name` and `description` frontmatter, then the body.
2. Optionally add `skills/<slug>/README.md` and `skills/<slug>/template.json`.
3. Run locally:
   ```bash
   python3 scripts/validate.py
   python3 scripts/build.py
   ```
4. Commit `skills/`, `index.json`, and regenerated `dist/`. Open a PR.

## CI

CI workflow is prepared but not installed: the current GitHub token lacks `workflow` scope and the workflow push failed. Until it can be installed, run `validate.py` and `build.py` locally before pushing.

## Upstream

`project-board-organizer` v2 is upgraded from [skill-asana-organizer](https://github.com/diamitani/skill-asana-organizer) (Claude Code skill, bash connectors, MCP server). That repo stays the Claude/script home; this monorepo is the multi-platform skill source.

## License

MIT © Patrick Diamitani, 2026
