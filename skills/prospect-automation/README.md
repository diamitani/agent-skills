# Prospect automation

Platform-agnostic upgrade of [prospector-skill](https://github.com/diamitani/prospector-skill), combining its root signal-to-email workflow, v0.3 corporate/local ICP routes and prospector-core deterministic SURE-list contract. Related prospect-pal is a web app scaffold; prospector-pal carries the earlier research contract. Neither replaces the skill source.

## Preserved behavior
Uploaded CSV/XLSX and signal/ICP intake; PAL planning; corporate and local-business discovery; role and event evidence; labeled pattern candidates; syntax/DNS checks; exact-approved verification; manual checker handoff; transparent scoring; SURE/Review/Rejected artifacts; suppression; optional approved CRM updates; bounded partial results.

## Grok Bot upgrades
Connector-first discovery (Apollo/HubSpot/Gmail/Sheets optional), secret-request rather than pasted keys, draft-only outreach, source-grounded contacts, CSV/XLSX or explicitly requested Google Sheet exports. No messages or CRM changes without exact approval. No subscriptions or live provider integrations are bundled.

## Implementation boundaries
The upstream deterministic judge/scripts remain upstream; this package contains reusable instructions, not executable adapters. Use a reviewed pinned upstream release or an equivalent trusted connector. Never treat a model-generated SURE label as deterministic proof. Root runtime and v0.3 specification differ; this version preserves the distinction between proof status and commercially ready_for_review.

Generated targets: Grok Bot, Claude, OpenAI, Cursor, Codex and Gemini. Read the full AGENTS.md on targets with instruction-length limits. Provider quotas, schemas and rights must be verified at execution.

Source content is adapted without personal accounts, contact datasets or credentials. MIT repository license; retain applicable upstream notices if distributing its code (none copied here).
