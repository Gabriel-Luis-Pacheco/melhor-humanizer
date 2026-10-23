#!/usr/bin/env python3
"""Static validation of the Agent Skill package; only reads files."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "melhor-humanizer"

def validate(root: Path = ROOT) -> list[str]:
    problems = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["SKILL.md ausente"]
    source = entry.read_text(encoding="utf-8")
    if not source.startswith("---\n") or "\n---\n" not in source[4:]:
        return ["Frontmatter não encontrado"]
    frontmatter = source[4:].split("\n---\n", 1)[0]
    name = re.search(r"(?m)^name:\s*([a-z][a-z0-9-]*)\s*$", frontmatter)
    desc = re.search(r'(?m)^description:\s*(.+?)\s*$', frontmatter)
    if not name or name.group(1) != NAME:
        problems.append("Nome de skill inválido")
    if not desc or not 1 <= len(desc.group(1).strip().strip('"')) <= 1024:
        problems.append("Descrição ausente ou maior que 1024 caracteres")
    if len(source.splitlines()) >= 500:
        problems.append("SKILL.md excede 500 linhas")
    for file in root.rglob("*.md"):
        body = file.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            dest = target.split("#", 1)[0]
            if dest and not (file.parent / dest).exists():
                problems.append(f"{file.relative_to(root)} aponta para caminho ausente: {dest}")
    return problems

if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print("ERRO:", problem)
    if not problems:
        print("Skill válida: frontmatter, tamanho e referências locais conferidos.")
    sys.exit(bool(problems))
