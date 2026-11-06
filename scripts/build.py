#!/usr/bin/env python3
"""Build platform-specific skill packs under dist/<platform>/<slug>/ from canonical SKILL.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)

PLATFORMS = ("grokbot", "claude", "openai", "cursor", "codex", "gemini")


def parse_skill(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    meta: dict[str, str] = {}
    raw_meta, body = match.group(1), match.group(2)
    key = None
    buf: list[str] = []
    for line in raw_meta.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line) and not line.startswith(" "):
            if key is not None:
                meta[key] = "\n".join(buf).strip().strip("'\"")
            key, _, rest = line.partition(":")
            key = key.strip()
            buf = [rest.strip()]
        else:
            buf.append(line.strip())
    if key is not None:
        meta[key] = "\n".join(buf).strip().strip("'\"")
    return meta, body.strip() + "\n"


def kebab(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", name.strip().lower())
    return re.sub(r"-+", "-", s).strip("-")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def connector_note(platform: str) -> str:
    notes = {
        "grokbot": (
            "## Platform notes (Grok Bot)\n"
            "- Prefer the installed Grok Bot / Cursor connector for the project tool over raw API tokens.\n"
            "- Authenticate a connector that needs sign-in; only request secrets if no connector can do the job.\n"
            "- Snapshots and previews live on the bot computer under `/workspace`.\n"
        ),
        "claude": (
            "## Platform notes (Claude Code / Agent Skills)\n"
            "- Prefer MCP or Claude connectors when available; otherwise use env tokens with "
            "`scripts/connectors.sh` from https://github.com/diamitani/skill-asana-organizer.\n"
            "- Never print PATs. Source helpers at the start of each bash block.\n"
        ),
        "openai": (
            "## Platform notes (OpenAI / Custom GPT / Codex)\n"
            "- Prefer Actions / MCP tools bound to the project system over pasting API tokens into chat.\n"
            "- If only HTTP Actions exist, map fetch/apply to those Actions; do not ask the user to curl.\n"
            "- Keep replies under product limits; put large previews in a downloadable artifact when possible.\n"
        ),
        "cursor": (
            "## Platform notes (Cursor)\n"
            "- Prefer installed MCP connectors for Asana and siblings over shell tokens.\n"
            "- Use the Cursor box/workspace for snapshots under `/workspace`.\n"
            "- Do not commit secrets; use Cursor secrets / env for any token fallback.\n"
        ),
        "codex": (
            "## Platform notes (Codex)\n"
            "- Prefer MCP or configured tools; fall back to repo `scripts/connectors.sh` with env tokens.\n"
            "- Keep the agent loop idempotent: preview, then apply only after confirmation.\n"
        ),
        "gemini": (
            "## Platform notes (Gemini)\n"
            "- Prefer Gemini extensions / tools if connected to the project system; otherwise guide the user "
            "through the skill-asana-organizer MCP server or API tokens as a last resort.\n"
            "- Chat-only surfaces: produce the full rewrite/section plan as copy-ready text when writes are unavailable.\n"
        ),
    }
    return notes[platform]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_grokbot(slug: str, name: str, description: str, body: str) -> None:
    content = (
        f"---\nname: {name}\ndescription: {yaml_quote(description)}\n---\n\n"
        f"{body.rstrip()}\n\n{connector_note('grokbot')}"
    )
    write(DIST / "grokbot" / slug / "SKILL.md", content)


def build_claude(slug: str, name: str, description: str, body: str) -> None:
    content = (
        f"---\nname: {kebab(name)}\ndescription: {yaml_quote(description)}\n---\n\n"
        f"{body.rstrip()}\n\n{connector_note('claude')}"
    )
    write(DIST / "claude" / slug / "SKILL.md", content)


def build_openai(slug: str, name: str, description: str, body: str) -> None:
    agents = (
        f"# {name}\n\n{description}\n\n{body.rstrip()}\n\n{connector_note('openai')}"
    )
    write(DIST / "openai" / slug / "AGENTS.md", agents)
    # Custom GPT instructions — hard cap 8000 chars
    instructions = (
        f"You are running the '{name}' skill.\n\n"
        f"When to use: {description}\n\n"
        f"{body.rstrip()}\n\n"
        f"{connector_note('openai')}"
    )
    if len(instructions) > 8000:
        instructions = instructions[:7997].rstrip() + "..."
    write(DIST / "openai" / slug / "instructions.md", instructions)


def build_cursor(slug: str, name: str, description: str, body: str) -> None:
    content = (
        f"---\ndescription: {yaml_quote(description)}\nglobs:\nalwaysApply: false\n---\n\n"
        f"# {name}\n\n{body.rstrip()}\n\n{connector_note('cursor')}"
    )
    write(DIST / "cursor" / slug / f"{kebab(name)}.mdc", content)


def build_codex(slug: str, name: str, description: str, body: str) -> None:
    content = f"# {name}\n\n{description}\n\n{body.rstrip()}\n\n{connector_note('codex')}"
    write(DIST / "codex" / slug / "AGENTS.md", content)


def build_gemini(slug: str, name: str, description: str, body: str) -> None:
    content = f"# {name}\n\n{description}\n\n{body.rstrip()}\n\n{connector_note('gemini')}"
    write(DIST / "gemini" / slug / "GEMINI.md", content)


BUILDERS = {
    "grokbot": build_grokbot,
    "claude": build_claude,
    "openai": build_openai,
    "cursor": build_cursor,
    "codex": build_codex,
    "gemini": build_gemini,
}


def main() -> int:
    if not SKILLS.is_dir():
        print("skills/ missing", file=sys.stderr)
        return 1

    # Clean previous dist for known platforms
    if DIST.exists():
        for platform in PLATFORMS:
            target = DIST / platform
            if target.exists():
                for path in sorted(target.rglob("*"), reverse=True):
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        path.rmdir()

    count = 0
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            print(f"skip {skill_dir.name}: no SKILL.md", file=sys.stderr)
            continue
        meta, body = parse_skill(skill_md.read_text(encoding="utf-8"))
        name = meta.get("name", "").strip()
        description = meta.get("description", "").strip()
        if not name or not description or not body.strip():
            print(f"skip {skill_dir.name}: incomplete SKILL.md", file=sys.stderr)
            continue
        slug = skill_dir.name
        for platform, builder in BUILDERS.items():
            builder(slug, name, description, body)
        count += 1

    print(f"built {count} skill(s) × {len(PLATFORMS)} platforms under dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
