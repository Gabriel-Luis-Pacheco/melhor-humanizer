#!/usr/bin/env python3
"""Inspect agent outputs against editorial case constraints. Not an AI detector.

Results are review flags, never pass/fail proof of writing quality.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import preserve

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{i}: JSON inválido: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{i}: cada linha precisa ser um objeto")
        rows.append(item)
    return rows

def validate_cases(cases: list[dict]) -> None:
    ids = set()
    required = {"id", "genre", "mode", "source", "prompt",
                "must_preserve", "red_flags", "control"}
    for case in cases:
        if not required.issubset(case):
            raise ValueError(f"Faltam campos em {case.get('id', '?')}: {required-set(case)}")
        if case["id"] in ids:
            raise ValueError(f"ID duplicado: {case['id']}")
        ids.add(case["id"])
        if case["mode"] not in ("edit", "audit", "create"):
            raise ValueError(f"Modo não reconhecido: {case['id']}")
        if not isinstance(case["control"], bool):
            raise ValueError(f"Controle deve ser booleano: {case['id']}")
        if not isinstance(case["must_preserve"], list) or not isinstance(case["red_flags"], list):
            raise ValueError(f"Restrições devem ser listas: {case['id']}")
    if len(cases) < 30:
        raise ValueError("Recomenda-se pelo menos 30 casos variados.")
    if sum(bool(c["control"]) for c in cases) * 3 < len(cases):
        raise ValueError("Ao menos 1/3 dos casos devem ser controles de não editar.")

def _flat(s: str) -> str:
    return re.sub(r"\s+", " ", s.casefold()).strip()

def evaluate(cases: list[dict], outputs: list[dict]) -> dict:
    lookup = {case["id"]: case for case in cases}
    records = []
    used = set()
    for result in outputs:
        identifier = result.get("id")
        candidate = result.get("candidate", "default")
        output = result.get("output")
        if identifier not in lookup:
            raise ValueError(f"ID não existe no corpus: {identifier}")
        if not isinstance(candidate, str) or not candidate:
            raise ValueError("candidate precisa ser uma string não vazia")
        if not isinstance(output, str):
            raise ValueError(f"output precisa ser texto: {identifier}")
        key = (candidate, identifier)
        if key in used:
            raise ValueError(f"Saída duplicada para candidate/id: {key}")
        used.add(key)
        case = lookup[identifier]
        flags = []
        normalized = _flat(output)
        for anchor in case["must_preserve"]:
            if _flat(anchor) not in normalized:
                flags.append({"kind": "required_text_missing", "detail": anchor})
        for phrase in case["red_flags"]:
            if _flat(phrase) in normalized:
                flags.append({"kind": "risky_phrase_present", "detail": phrase})
        if case["mode"] == "edit":
            comparison = preserve.compare(case["source"], output)
            if comparison["review_required"]:
                flags.append({
                    "kind": "preservation_warning",
                    "detail": {
                        "missing_anchors": comparison["missing_anchors"],
                        "added_anchors": comparison["added_anchors"],
                        "semantic_cues": comparison["semantic_cues"],
                    },
                })
            if case["control"]:
                similarity = difflib.SequenceMatcher(None, case["source"], output).ratio()
                if similarity < 0.65:
                    flags.append({"kind": "possible_overediting", "detail": round(similarity, 3)})
        records.append({"candidate": candidate, "id": identifier,
                        "control": case["control"], "review_flags": flags})
    counts = Counter(r["candidate"] for r in records)
    return {
        "cases_available": len(cases),
        "outputs_received": dict(counts),
        "outputs_needing_review": sum(bool(r["review_flags"]) for r in records),
        "results": records,
        "disclaimer": ("Alertas automatizados são aproximações. Uma reescrita equivalente "
                       "pode ser sinalizada e uma alteração de significado pode passar despercebida. "
                       "Use a avaliação cega por pessoas antes de declarar superioridade."),
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Auxílio para avaliação de reescritas")
    parser.add_argument("results", nargs="?", help="JSONL com id, output e candidate opcional")
    parser.add_argument("--corpus", type=Path, default=ROOT/"eval/casos.jsonl")
    parser.add_argument("--validate-corpus", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Falhar quando existirem alertas")
    args = parser.parse_args(argv)
    try:
        cases = load_jsonl(args.corpus)
        validate_cases(cases)
        if args.validate_corpus:
            print(f"Corpus validado: {len(cases)} casos; "
                  f"{sum(bool(c['control']) for c in cases)} controles.")
            return 0
        if not args.results:
            parser.error("Informe results.jsonl ou --validate-corpus.")
        report = evaluate(cases, load_jsonl(Path(args.results)))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Respostas avaliadas: {sum(report['outputs_received'].values())}")
        print(f"Com alertas para revisão: {report['outputs_needing_review']}")
        for row in report["results"]:
            if row["review_flags"]:
                names = ", ".join(x["kind"] for x in row["review_flags"])
                print(f"  {row['candidate']}/{row['id']}: {names}")
        print(report["disclaimer"])
    return int(args.strict and report["outputs_needing_review"] > 0)

if __name__ == "__main__":
    raise SystemExit(main())
