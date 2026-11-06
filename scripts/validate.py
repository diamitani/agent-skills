#!/usr/bin/env python3
"""Validate skills/*/SKILL.md frontmatter and regenerate index.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
INDEX = ROOT / "index.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter delimited by ---")
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
    return meta, body


def main() -> int:
    if not SKILLS.is_dir():
        print("skills/ directory missing", file=sys.stderr)
        return 1

    entries = []
    errors = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        slug = skill_dir.name
        if not skill_md.is_file():
            errors.append(f"{slug}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        try:
            meta, body = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"{slug}: {exc}")
            continue
        name = meta.get("name", "").strip()
        description = meta.get("description", "").strip()
        if not name:
            errors.append(f"{slug}: frontmatter missing name")
        if not description:
            errors.append(f"{slug}: frontmatter missing description")
        if not body.strip():
            errors.append(f"{slug}: empty body after frontmatter")
        if name and description and body.strip():
            entries.append(
                {
                    "slug": slug,
                    "name": name,
                    "description": description,
                    "path": f"skills/{slug}/SKILL.md",
                }
            )

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    INDEX.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"validated {len(entries)} skill(s); wrote {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
