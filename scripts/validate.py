#!/usr/bin/env python3
"""Validate the powerclaw skill: strict frontmatter and cross-references."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
errors = []
text = SKILL.read_text(encoding="utf-8")

if not text.startswith("---\n") or text.find("\n---", 4) == -1:
    errors.append("SKILL.md must have closed '---' frontmatter")
else:
    block = text[4:text.find("\n---", 4)]
    try:
        import yaml
        fm = yaml.safe_load(block) or {}
    except Exception as e:
        errors.append(f"frontmatter is not valid strict YAML: {e}"); fm = {}
    name = str(fm.get("name", ""))
    desc = str(fm.get("description", ""))
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name): errors.append(f"bad name: {name!r}")
    if any(w in name for w in ("anthropic", "claude")): errors.append("name contains reserved word")
    if not desc or len(desc) > 1024: errors.append("description missing or over 1024 chars")
    if re.search(r"<[a-zA-Z/][^>]*>", desc): errors.append("description contains XML tags")

if text.count("\n") + 1 > 500: errors.append("SKILL.md over 500 lines")

referenced = set(re.findall(r"`?(references/[A-Za-z0-9._-]+\.md)`?", text))
for rel in sorted(referenced):
    if not (ROOT / rel).is_file(): errors.append(f"missing referenced file: {rel}")
for f in sorted((ROOT / "references").glob("*.md")):
    if f"references/{f.name}" not in referenced: errors.append(f"references/{f.name} not referenced from SKILL.md")

if errors:
    print(f"FAIL: {len(errors)}"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"OK: frontmatter valid, {len(referenced)} cross-references resolve")
