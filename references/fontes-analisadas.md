# Pesquisa comparativa de projetos públicos

Revisão inicial em 23/10/2026. Os projetos abaixo foram encontrados e tiveram seus arquivos principais inspecionados no GitHub; alguns scripts e arquivos de avaliação também foram examinados. Não foram executadas suítes completas de terceiros nem auditado cada arquivo de todos os repositórios. “Melhor” aqui significa adequação aos objetivos deste projeto, não um ranking objetivo universal.

A implementação deste repositório é **original**: aproveita critérios editoriais e ideias gerais, não reproduz em bloco textos, código ou catálogos de outra skill. Consulte as licenças e os autores originais antes de reaproveitar material externo.

| Projeto | O que foi examinado | Melhor contribuição observada | Limite ou cuidado |
| --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | SKILL.md, README, árvore e versões | Distingue pistas fortes de pistas fracas; edição por sentido; defesa de fatos e voz | Inglês como eixo principal; listas não bastam para avaliar texto brasileiro. |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | SKILL.md e structures.md | Tira contrastes vazios, aberturas, falsos agentes e frases de efeito | Banir todo advérbio ou passiva pode mudar fatos ou registro. |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | SKILL.md e eval.md | Edição mínima, teste de portabilidade e revisão adversarial | A avaliação final precisa de julgamento humano. |
| [ameenmo/humanize-skill](https://github.com/ameenmo/humanize-skill) | SKILL.md e eval.md | Modos preservar/conformar, revisão sem fabricar dados, defesa contra over-edit | Algumas preferências tipográficas são relativas ao estilo do autor. |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | SKILL.md, metrics.js e facts.js | Combina perfis de voz, métricas de ritmo e preservação de tokens concretos | Pontuação de “AI-tells” não equivale a probabilidade de autoria. |
| [jooray/humanizer](https://github.com/jooray/humanizer) | SKILL.md e forensic_residue.py | Catálogo extenso e distinção entre revisão editorial e resíduos mecânicos | Muitas regras aumentam chance de falsos positivos sem contexto. |
| [d-wwei/great-writer](https://github.com/d-wwei/great-writer) | SKILL.md, árvore de módulos | Roteamento por gênero e processo de revisão | Complexidade excessiva pode atrapalhar pedidos simples. |
| [Tradelord223/plain-english](https://github.com/Tradelord223/plain-english) | SKILL.md e behavior-contract.md | Contrato preciso de incerteza, obrigação, status e termos técnicos | Foco mais técnico que literário. |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | SKILL.md | Escrita acadêmica precisa e baseada em evidências; sem personalidade fabricada | Modo acadêmico não deve ser padrão para mensagens. |
| [machinemade-mm/humanmade-antislop](https://github.com/machinemade-mm/humanmade-antislop) | SKILL.md e árvore de referências | Rigor de relatório, estrutura científica, vieses e argumentação | Regras absolutas de vocabulário e apresentação não servem a todo texto. |
| [ehmo/slopkit](https://github.com/ehmo/slopkit) | Slopbeth SKILL.md e evaluation.md | Benchmark com casos de controle, retenção semântica e falsos positivos | Testes publicamente descritos não validam automaticamente outra skill. |
| [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) | SKILL.md e árvore | Atenção a repetição, tamanho de frases e palavras de vitrine | Proibições sem exceção achatam a voz autoral. |
| [mackswendhell/humanizer-pt-br](https://github.com/mackswendhell/humanizer-pt-br) | SKILL.md | Repertório específico de expressões, ritmo e falsos cognatos no português | “Injetar personalidade” sem fonte pode fabricar opinião. |
| [rpiochi/humanizer-pt-br](https://github.com/rpiochi/humanizer-pt-br) | SKILL.md | Conectivos, anglicismos e encerramentos motivacionais de PT-BR | Traduções de padrões ingleses precisam de adaptação, não cópia. |
| [eric-tramel/slop-guard](https://github.com/eric-tramel/slop-guard) | README.md e catálogo de regras | Lint programático auditável e alertas localizados | Heurística textual não é prova de IA nem substitui revisão. |

## Princípios adotados após a comparação

1. Preservação semântica acima de “fluência”.
2. Brasil como idioma de primeira classe; inglês como alternativa.
3. Regra editorial com contexto e falsos positivos explícitos.
4. Revisões mínimas por padrão; reestruturação só quando necessária.
5. Tratamento próprio por gênero e tipo de artefato.
6. Ferramentas opcionais, locais e conservadoras, sem reescrita automática.
7. Casos de avaliação incluindo textos humanos já bons e exemplos de dano por over-edit.
8. Nenhum resultado prometido em detectores de autoria.

## Referências conceituais adicionais

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): repertório colaborativo de traços recorrentes, não método de identificação determinística.
- [Agent Skills specification](https://agentskills.io/specification): organização SKILL.md, referências e scripts.
- [Plain language principles](https://www.plainlanguage.gov/guidelines/): clareza guiada pelas necessidades do leitor.

A seleção pode ser ampliada com novas evidências e testes de comportamento. Nunca declare que esta skill “vence todas as outras” sem uma comparação reproduzível com dados, controle e critérios previamente fixados.
