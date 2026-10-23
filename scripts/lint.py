#!/usr/bin/env python3
"""Local prose-quality hints. NOT a detector of AI authorship.

Python 3.10+, standard library only. Never rewrites input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    line: int
    snippet: str
    suggestion: str

# An intentionally selective bank; patterns are clues requiring human judgment.
RULES = {
    "pt": [
        ("chatbot_open", "alta", r"(?i)\b(?:claro[!,.:]|excelente pergunta|vamos (?:mergulhar|explorar|desvendar)|aqui est[aá] (?:o|a|um|uma))\b", "Remova a abertura e vá ao assunto, se ela não cumprir uma função."),
        ("empty_preamble", "media", r"(?i)\b(?:[eé] importante (?:ressaltar|destacar|salientar)|vale (?:destacar|ressaltar)|cabe salientar|em um mundo cada vez mais)\b", "Diga a informação diretamente."),
        ("fake_reversal", "alta", r"(?i)\b(?:n[aã]o (?:[eé]|se trata) (?:apenas|s[oó]|somente))\b.{0,100}\b(?:mas|e sim)\b", "Verifique se o contraste é necessário; caso contrário, afirme o ponto."),
        ("sales_fluff", "media", r"(?i)\b(?:jornada transformadora|desbloque(?:ar|ie) (?:todo )?o potencial|novo patamar|revolu[cç][aã]o|experi[eê]ncia [uú]nica|solu[cç][aã]o robusta)\b", "Troque promessa genérica por fato demonstrado ou retire."),
        ("filler_link", "media", r"(?i)\b(?:nesse contexto|diante desse cen[aá]rio|ademais|outrossim|por conseguinte|em suma)\b", "Confira se este conector realmente marca uma relação."),
        ("fake_authority", "alta", r"(?i)\b(?:especialistas (?:comprovam|afirmam)|estudos (?:comprovam|mostram)|segundo especialistas)\b", "Informe a fonte real ou remova a atribuição sem prova."),
        ("superficial_end", "media", r"(?i),?\s*(?:refor[cç]ando a import[aâ]ncia|evidenciando a relev[aâ]ncia)\b", "Descreva uma consequência sustentada ou elimine a frase."),
        ("generic_ending", "media", r"(?i)\b(?:o futuro [eé] promissor|e isso muda tudo|o resultado fala por si|essa [eé] a verdadeira transforma[cç][aã]o)\b", "Encerre no último dado ou ação útil."),
        ("stock_motivation", "media", r"(?i)\b(?:transformar desafios em oportunidades|cada detalhe foi pensado|muito mais do que)\b", "Escolha uma informação específica, se houver."),
        ("overexplaining", "media", r"(?i)\b(?:neste (?:artigo|texto|par[aá]grafo) (?:vamos|iremos)|a seguir (?:apresentaremos|veremos))\b", "Retire o anúncio e comece o conteúdo."),
    ],
    "en": [
        ("chatbot_open", "alta", r"(?i)\b(?:great question|let.s dive in|here.s the thing|i hope this helps)\b", "State the point instead of introducing it."),
        ("fake_reversal", "alta", r"(?i)\bit.s not (?:just|only)\b.{0,100}\bit.s\b", "Check whether the contrast is informative."),
        ("empty_preamble", "media", r"(?i)\b(?:it.s important to note|at its core|in today.s fast.paced world|let that sink in)\b", "Remove staging and state what matters."),
        ("sales_fluff", "media", r"(?i)\b(?:game.changing|unlock the power of|seamless experience|transformative journey)\b", "Use substantiated specifics, not grand language."),
        ("generic_ending", "media", r"(?i)\b(?:and that changes everything|the future is bright)\b", "End on the last useful fact or action."),
    ]
}

FENCE = chr(96) * 3
INLINE = chr(96)
URL = re.compile(r"https?://[^\s)]+", re.I)
MD_LINK = re.compile(r"\[[^]\n]+\]\([^)]+\)")
QUOTE = re.compile(r'["“][^"”\n]{1,220}["”]')
WORD = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*", re.UNICODE)
REVIEW_LINE = re.compile(r"(?m)^\s*[-*]\s+\*\*[^*]{2,65}\*\*\s*[:—–-]")

def language_of(text: str) -> str:
    """Default to pt-BR unless unmistakably English."""
    pt = len(re.findall(r"\b(?:que|para|com|não|uma|isso|pelo|está|também)\b", text, re.I))
    en = len(re.findall(r"\b(?:the|that|with|from|this|there|your|have|does)\b", text, re.I))
    return "en" if en > pt * 2 and en >= 3 else "pt"

def mask_inline(line: str) -> str:
    """Keep columns stable so reported excerpts still match the source."""
    patterns = [
        re.compile(re.escape(INLINE) + r"[^" + re.escape(INLINE) + r"\n]+" + re.escape(INLINE)),
        URL, MD_LINK, QUOTE,
    ]
    for pattern in patterns:
        line = pattern.sub(lambda m: " " * len(m.group()), line)
    return line

def lint_text(text: str, lang: str = "auto") -> list[Finding]:
    if lang == "auto":
        lang = language_of(text)
    found: list[Finding] = []
    fenced = False
    frontmatter = False
    for number, raw in enumerate(text.splitlines(), 1):
        trimmed = raw.strip()
        if number == 1 and trimmed == "---":
            frontmatter = True
            continue
        if frontmatter:
            if trimmed == "---":
                frontmatter = False
            continue
        if trimmed.startswith((FENCE, "~~~")):
            fenced = not fenced
            continue
        if fenced or not trimmed or trimmed.startswith((">", "#", "|", "//")):
            continue
        masked = mask_inline(raw)
        for rule, severity, pattern, advice in RULES[lang]:
            if re.search(pattern, masked):
                found.append(Finding(rule, severity, number, raw.strip()[:180], advice))
        if REVIEW_LINE.search(masked):
            found.append(Finding("labels_in_lists", "baixa", number, raw.strip()[:180],
                                 "Confira se os rótulos em negrito ajudam a ler ou são decoração."))
        # Density matters: one isolated dash is not a finding.
        if masked.count("—") >= 3 and len(WORD.findall(masked)) < 160:
            found.append(Finding("dash_density", "baixa", number, raw.strip()[:180],
                                 "Revise a repetição de travessões; preserve os necessários."))
    return found

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dicas de edição, não detector de autoria.")
    p.add_argument("file", help="Arquivo UTF-8 ou - para stdin")
    p.add_argument("--lang", choices=("auto", "pt", "en"), default="auto")
    p.add_argument("--json", action="store_true", help="Saída estruturada")
    p.add_argument("--strict", action="store_true", help="Sair com 1 se encontrar alertas altos")
    args = p.parse_args(argv)
    try:
        content = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        p.error(str(exc))
    findings = lint_text(content, lang=args.lang)
    if args.json:
        print(json.dumps({"findings": [asdict(f) for f in findings],
                          "warning": "Heurística editorial: não determina autoria."},
                         ensure_ascii=False, indent=2))
    elif not findings:
        print("Nenhum padrão catalogado encontrado. Isso não comprova qualidade nem autoria.")
    else:
        for f in findings:
            print(f"L{f.line} [{f.severity}] {f.rule}: {f.snippet}\n  Sugestão: {f.suggestion}")
        print(f"\n{len(findings)} alerta(s) para leitura contextual; nenhum é prova de autoria.")
    return 1 if args.strict and any(f.severity == "alta" for f in findings) else 0

if __name__ == "__main__":
    raise SystemExit(main())
