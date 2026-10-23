#!/usr/bin/env python3
"""Conservative literal-anchor check between original and rewrite.

Does not claim semantic equivalence. Reports lexical risk cues as well as anchors.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

# These are review cues, not a natural-language inference engine.
CUES = {
    "negation_scope": re.compile(r"\b(?:não|nunca|jamais|sem|exceto|somente|apenas|todos|nenhum|alguns|not|never|without|except|only|all|none)\b", re.I),
    "modality_uncertainty": re.compile(r"\b(?:pode|podem|poderá|poderia|deve|devem|deverá|precisa|obrigatório|possível|provável|talvez|possivelmente|may|might|must|should|could|likely)\b", re.I),
    "operational_state": re.compile(r"\b(?:será|serão|foi|foram|planejado|previsto|pendente|concluído|aprovado|testado|verificado|publicado|implantado|planned|pending|completed|verified|tested|deployed)\b", re.I),
}

# Priority order matters; matched spans are blanked before later extraction.
TOKENS = [
    ("url", re.compile(r"https?://[^\s<>\x22\x27]+", re.I)),
    ("email", re.compile(r"(?<![\w.])[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)),
    ("code", re.compile(re.escape(chr(96)) + r"[^" + re.escape(chr(96)) + r"\n]+" + re.escape(chr(96)))),
    ("date", re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)|(?<!\d)\d{1,2}/\d{1,2}/\d{2,4}(?!\d)")),
    ("cnpj_cpf", re.compile(r"(?<!\d)(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2})(?!\d)")),
    ("money", re.compile(r"(?i)(?:R\$\s*|US\$\s*|€\s*)-?\d+(?:[.,]\d+)*")),
    ("percent", re.compile(r"(?<![\w\d])-?\d+(?:[.,]\d+)?\s*%")),
    ("ip", re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")),
    ("number", re.compile(r"(?<![\w])-?\d+(?:[.,]\d+)*(?![\w])")),
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
                while token.endswith(")") and token.count(")") > token.count("("):
                    token = token[:-1].rstrip(".,;:!?")
            if kind == "cnpj_cpf":
                token = re.sub(r"\D", "", token)
            if kind in ("money", "percent"):
                token = re.sub(r"\s+", "", token)
            hits[token] += 1
            return " " * len(m.group())
        state = pattern.sub(capture, state)
        collected[kind] = hits
    return collected


def _prose_cues(text: str) -> dict[str, Counter[str]]:
    """Skip code fences and inline code to reduce misleading cue differences."""
    lines = []
    in_fence = False
    delimiter = ""
    fence_size = 0
    for raw in text.splitlines():
        match = re.match(r"^ {0,3}(" + chr(96) + r"{3,}|~{3,})(.*)$", raw)
        if match:
            candidate, tail = match.groups()
            if not in_fence:
                in_fence, delimiter, fence_size = True, candidate[0], len(candidate)
            elif candidate[0] == delimiter and len(candidate) >= fence_size and not tail.strip():
                in_fence = False
            continue
        if in_fence:
            continue
        raw = re.sub(chr(96) + r"+[^" + chr(96) + r"\n]+" + chr(96) + r"+", "", raw)
        raw = re.sub(r"https?://\S+", "", raw)
        lines.append(raw)
    plain = "\n".join(lines)
    return {kind: Counter(m.group().casefold() for m in regex.finditer(plain))
            for kind, regex in CUES.items()}

def compare(before: str, after: str) -> dict[str, object]:
    old, new = anchors(before), anchors(after)
    missing, added = {}, {}
    for kind in old:
        lost, gained = old[kind] - new[kind], new[kind] - old[kind]
        if lost:
            missing[kind] = dict(sorted(lost.items()))
        if gained:
            added[kind] = dict(sorted(gained.items()))
    left, right = _prose_cues(before), _prose_cues(after)
    semantic_cues = {}
    for kind in CUES:
        dropped = left[kind] - right[kind]
        introduced = right[kind] - left[kind]
        if dropped or introduced:
            semantic_cues[kind] = {"removed": dict(sorted(dropped.items())), "added": dict(sorted(introduced.items()))}
    return {
        "review_required": bool(missing or added or semantic_cues),
        "semantic_cues": semantic_cues,
        "missing_anchors": missing,
        "added_anchors": added,
        "limitations": ("Compara tokens e palavras-sinal; não prova equivalência semântica. "
                        "Mudanças legítimas podem gerar alertas; ausência de alertas não valida "
                        "fatos, atribuições, modalidade, negações, escopo ou sentido."),
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
            for category, detail in result["semantic_cues"].items():
                print(f"  Possível mudança de {category}: {detail}")
        print(result["limitations"])
    return int(args.strict and result["review_required"])

if __name__ == "__main__":
    raise SystemExit(main())
