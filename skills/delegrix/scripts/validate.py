#!/usr/bin/env python3
"""Offline static validation for the Delegrix skill package.

Only stdlib required; YAML parsing is optional if PyYAML happens to be installed.
This is NOT a live subagent-runtime test.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def main() -> int:
    errors = []
    source = SKILL.read_text(encoding="utf-8")
    match = re.match(r"\A---\n([\s\S]*?)\n---\n", source)
    if not match:
        errors.append("missing YAML frontmatter")
        frontmatter = ""
    else:
        frontmatter = match.group(1)
        nm = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.M)
        if not nm or nm.group(1) != ROOT.name:
            errors.append("frontmatter name must match directory name")
        ds = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        if not ds or not (1 <= len(ds.group(1)) <= 1024):
            errors.append("description required, 1–1024 chars")
        if not re.search(r"^\s*version:\s*['\"]?0\.1\.0", frontmatter, re.M):
            errors.append("expected skill version 0.1.0")
    for relative in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", source):
        if "://" not in relative and not (ROOT / relative).is_file():
            errors.append(f"missing SKILL.md reference {relative}")
    for path in (ROOT / "references").glob("*.md"):
        for relative in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if "://" not in relative and not (path.parent / relative).is_file():
                errors.append(f"missing reference in {path.name}: {relative}")
    manifest = ROOT / "agents" / "openai.yaml"
    if not manifest.exists():
        errors.append("missing agents/openai.yaml")
    else:
        meta = manifest.read_text(encoding="utf-8")
        for key in ("interface:", "display_name:", "short_description:", "default_prompt:", "policy:"):
            if key not in meta:
                errors.append(f"missing UI metadata: {key}")
        try:
            import yaml
        except ImportError:
            pass
        else:
            try:
                d = yaml.safe_load(meta)
                if d["policy"]["allow_implicit_invocation"] is not True:
                    errors.append("unexpected implicit invocation policy")
            except Exception as exc:
                errors.append(f"agents/openai.yaml invalid: {exc}")
    must_mention = ["authorization", "ForgeGuard", "ForgeScope", "AGENTS.md", "ownership", "handoff", "integration", "runtime", "verification", "worker"]
    for concept in must_mention:
        if concept.casefold() not in source.casefold():
            errors.append(f"missing core concept: {concept}")
    if len(source.splitlines()) > 500:
        errors.append("SKILL.md should remain <= 500 lines")
    # No file may try to install or modify CLI settings automatically.
    if errors:
        print("FAIL")
        for error in errors:
            print(" -", error)
        return 1
    print(f"PASS: {ROOT.name} v0.1.0; {len(list(ROOT.rglob('*')))} entries; {len(source.splitlines())} SKILL.md lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
