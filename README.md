# grokbot-skills

Source of truth for **Grok Bot** skills maintained by [Patrick Diamitani](https://github.com/diamitani).

One folder per skill under `skills/<slug>/`. Each skill has a required `SKILL.md` (YAML frontmatter + recipe body) and may include a `README.md` or `template.json`.

## Skills

| Slug | Name | Description |
|------|------|-------------|
| [project-board-organizer](skills/project-board-organizer/) | project-board-organizer | Audit and clean messy project boards (Asana, ClickUp, Monday, Trello, Notion, Jira): rewrite tasks for an audience, reorganize sections, preview before apply. |

## How to add a skill

1. Create `skills/<slug>/SKILL.md` with frontmatter keys `name` and `description`, then the markdown body.
2. Optionally add `skills/<slug>/README.md` (human docs) and `skills/<slug>/template.json` (bot template metadata).
3. Run `python3 scripts/validate.py` — it checks every skill and writes `index.json`.
4. Open a PR. CI runs the same validator on push and pull requests.

## Index

`scripts/validate.py` regenerates `index.json` with `{slug, name, description, path}` for each skill. Treat that file as generated.

## License

MIT © Patrick Diamitani, 2026
