#!/usr/bin/env python3
"""Conservative literal-anchor check between original and rewrite.

Does not claim semantic equivalence. Emits review flags only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Priority order matters; matched spans are blanked before later extraction.
TOKENS = [
    ("url", re.compile(r"https?://[^\s<>()\]]+", re.I)),
    ("email", re.compile(r"(?<![\w.])[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)),
    ("code", re.compile(re.escape(chr(96)) + r"[^" + re.escape(chr(96)) + r"\n]+" + re.escape(chr(96)))),
    ("date", re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)|(?<!\d)\d{1,2}/\d{1,2}/\d{2,4}(?!\d)")),
    ("cnpj_cpf", re.compile(r"(?<!\d)(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2})(?!\d)")),
    ("money", re.compile(r"(?i)(?:R\$\s*|US\$\s*|€\s*)\d+(?:[.,]\d+)*")),
    ("percent", re.compile(r"(?<!\w)\d+(?:[.,]\d+)?\s*%")),
    ("ip", re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")),
    ("number", re.compile(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])")),
]

def anchors(text: str) -> dict[str, Counter[str]]:
    state = text
    collected: dict[str, Counter[str]] = {}
    for kind, pattern in TOKENS:
        hits: Counter[str] = Counter()
        def capture(m: re.Match[str]) -> str:
            token = m.group().strip()
            # punctuation after a URL is prose punctuation
            if kind == "url":
                token = token.rstrip(".,;:!?")
            if kind == "cnpj_cpf":
                token = re.sub(r"\D", "", token)
            hits[token] += 1
            return " " * len(m.group())
        state = pattern.sub(capture, state)
        collected[kind] = hits
    return collected

def compare(before: str, after: str) -> dict[str, object]:
    old, new = anchors(before), anchors(after)
    missing, added = {}, {}
    for kind in old:
        lost, gained = old[kind] - new[kind], new[kind] - old[kind]
        if lost:
            missing[kind] = dict(sorted(lost.items()))
        if gained:
            added[kind] = dict(sorted(gained.items()))
    return {
        "review_required": bool(missing or added),
        "missing_anchors": missing,
        "added_anchors": added,
        "limitations": ("Compara tokens literais, não fatos nem equivalência semântica. "
                        "Mudanças legítimas de representação podem produzir alertas; "
                        "nomes próprios, modalidade, negações e sentido exigem revisão humana."),
    }

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compare âncoras literais sem reescrever arquivos.")
    p.add_argument("original", help="Arquivo UTF-8 original")
    p.add_argument("revision", help="Arquivo UTF-8 revisado")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true", help="Sair com 1 se houver diferenças")
    args = p.parse_args(argv)
    try:
        before = Path(args.original).read_text(encoding="utf-8")
        after = Path(args.revision).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        p.error(str(exc))
    result = compare(before, after)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result["review_required"]:
            print("Nenhuma diferença nas âncoras catalogadas. Revise o sentido manualmente.")
        else:
            print("Diferenças que precisam de conferência:")
            for title, key in (("Ausentes", "missing_anchors"), ("Novas", "added_anchors")):
                for category, items in result[key].items():
                    print(f"  {title} em {category}: {items}")
        print(result["limitations"])
    return int(args.strict and result["review_required"])

if __name__ == "__main__":
    raise SystemExit(main())
