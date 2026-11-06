# project-board-organizer

Use when someone wants a messy project board (Asana, ClickUp, Monday, Trello, Notion, or Jira) audited and cleaned up: tasks rewritten for a specific audience and sections reorganized, with a preview before anything changes.

# Project board organizer (v2)

Turns a messy project board into a stakeholder-ready one: audits it, rewrites every task for a chosen audience, proposes a clean section structure, and applies the approved changes. Works with Asana, ClickUp, Monday, Trello, Notion, and Jira. Never deletes tasks. Upgraded from the open-source skill at https://github.com/diamitani/skill-asana-organizer (its `scripts/connectors.sh` and `mcp/server.py` are a fallback API layer).

Run it yourself; never ask the user to type a command.

## Step 1: Detect the tool and get access
- From the URL: app.asana.com = Asana (project id is the number after `/0/` or `/project/`), app.clickup.com = ClickUp, *.monday.com = Monday, trello.com = Trello, notion.so = Notion, *.atlassian.net = Jira.
- Prefer that tool's connector. If installed but needs sign-in, authenticate it; if missing, search plugins and install it.
- Only if no connector exists: request the token as a secret (ASANA_PAT, CLICKUP_API_TOKEN, MONDAY_API_TOKEN, TRELLO_API_KEY + TRELLO_API_TOKEN, NOTION_API_KEY, or JIRA_BASE_URL + JIRA_EMAIL + JIRA_API_TOKEN), clone the repo above to /workspace, and use `source scripts/connectors.sh` with `connect_<tool>_fetch_project` and `connect_<tool>_apply_changes`. Never print a token.

## Step 2: Fetch and snapshot
Fetch the project, all sections, and all tasks (open and completed, paginate past 100/200): name, notes, assignee, due date, completed, section membership, custom fields, dependencies, subtasks count. Save the raw result to `/workspace/<project-id>-before-<date>.json` as the rollback snapshot.

## Step 3: Health audit (show this first)
Report: project name; total / open / completed tasks; sections and their names; overdue tasks (due before today, not completed); tasks with no assignee; tasks with no due date; likely duplicates (near-identical names); empty sections; vague names (under 4 words, abbreviations, "stuff", "misc", "TBD"). Keep it to a short summary.

## Step 4: Requirements
If audience and grouping weren't given, ask one question covering both. Defaults if they say "you pick": cross-functional, group by status. Patterns:
- "For my boss": clean sections, verb-first, status on top. "For exec/leadership": impact-first, no jargon. "Cross-functional": owner in name, dependencies called out.
- Group by status: Blocked / Needs Decision, In Progress, Up Next (This Week), Backlog, Completed. By priority: Critical, High Priority, This Week, Backlog. By team: one section per team or owner. By deadline: Overdue, This Week, This Month, Later, No Date.

## Step 5: Rewrite tasks
Name rules: verb-first; outcome-focused; under 80 characters; no jargon unfamiliar to the audience; consistent format.
Notes rules (max 3 sentences): What it involves; Why it matters; Done when (acceptance criteria). Preserve any existing links, checklists, or details by appending the original notes below a line `Original notes:` rather than discarding them.
Never invent facts: no made-up dates, owners, customers, or scope. If a rewrite needs a fact that's missing, keep it generic and list it under "Questions for the owner".

Style by audience:
| Audience | Name example | Notes focus |
|---|---|---|
| Executive | Finalize Q2 product roadmap for board | Business outcome |
| Direct manager | Complete API migration to v3 | What, ETA, blockers |
| Cross-functional | Design team: Review homepage mockups | Owner and dependencies |
| Engineering | Migrate auth service to OAuth 2.0 | Technical acceptance criteria |
| Sales/GTM | Send proposal to Acme Corp by Friday | Deal and revenue context |

Templates: Deliver [outcome] by [deadline]; Review and approve [thing] ([owner]); Decide on [topic], needs [stakeholder]; Send [what] to [who] by [when]; Build [feature] for [purpose]; Launch [thing] to [audience]; Fix [issue] blocking [downstream]. Example: "backend deploy stuff - prd" becomes "Deploy backend services to production".

## Step 6: Propose structure and preview
Design sections for the grouping. Blocked and urgent first, completed last. Reuse existing sections with matching names; never create duplicates. Show one preview: before/after table of task names (with note rewrites for the first few, all available on request), the section map with task counts, which tasks move, and the open questions. For boards over ~50 tasks, put the full preview in a file or Page and summarize in chat. Wait for an explicit yes; accept partial approvals ("apply names only", "skip section changes", "exclude task X").

## Step 7: Apply
In this order: create missing sections, apply rewrites, move tasks. Change only name, notes, and section membership. Never delete tasks or sections; never change assignees, due dates, custom fields, or completion unless the user explicitly asks. Confirm each call succeeds; on a failure, log it and continue with the rest. Skip changes already in place, so a rerun is safe.

## Step 8: Verify and report
Re-fetch and confirm each change landed. Report: rewrites applied, sections created, tasks moved, failures, the new structure with counts, the open questions, and a link to the project. Offer: rollback from the snapshot (restores names, notes, and sections), and a weekly routine to re-tidy before a recurring review.

## Rules
- Preview before any write; never delete; never expose tokens.
- Empty sections left behind are reported, not deleted, unless the user asks.
- Triggers: "organize this [URL]", "clean up my board", "rewrite these tasks for leadership", "group tasks by team/status/priority", "this project is a mess".

## Platform notes (OpenAI / Custom GPT / Codex)
- Prefer Actions / MCP tools bound to the project system over pasting API tokens into chat.
- If only HTTP Actions exist, map fetch/apply to those Actions; do not ask the user to curl.
- Keep replies under product limits; put large previews in a downloadable artifact when possible.
