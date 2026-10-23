# Avaliação cega e replicável

## Por que não medir “humanidade” por detector

Um detector de texto automatizado pode produzir falsos positivos e negativos; ele não diz se um relatório preservou fatos, se o autor se reconhece no texto ou se a mensagem ficou mais útil. Não reporte “99% humano”. O alvo editorial é utilidade, precisão e voz.

## Como comparar versões

Selecione no mínimo 30 pedidos variados, separados **antes** dos testes, com pelo menos 1/3 de controles onde a melhor alteração é mínima ou nenhuma. Conte entre eles PT-BR formal, PT-BR informal, texto técnico, documento escolar, marketing, instruções, texto pessoal e texto já bom.

Para cada caso:
1. Gere a saída de cada candidato com o **mesmo pedido**, materiais e limites; sem revelar ao avaliador de qual skill veio.
2. Embaralhe as versões e solicite uma avaliação por critérios, não só preferência geral.
3. Verifique separadamente os invariantes bloqueantes.
4. Peça ao menos duas avaliações independentes se for publicar comparações.
5. Resolva discordâncias olhando para textos e evidências, não para marca ou prestígio da skill.

## Ficha de avaliação

### Portões bloqueantes: falha em qualquer um impede aprovação

- Fato novo ou alterado que não existia no material original.
- Mudança de escopo, negação, condição, prazo ou grau de certeza.
- Atribuição ou vivência inventada.
- Mudança não pedida de estrutura obrigatória, código, fórmula ou dado.
- Falsa promessa de desempenho em detector.

### Aspectos de 0 a 4

0 = falha grave; 1 = fraco; 2 = aceitável; 3 = bom; 4 = excelente.

| Critério | Pergunta |
| --- | --- |
| Legibilidade | O leitor entende com facilidade, sem esforço que não acrescenta valor? |
| Voz e contexto | O texto cabe na situação e preserva os traços dados pelo autor? |
| Densidade informativa | Cada passagem contribui com fato, ideia, efeito ou ação? |
| Composição | Ordem, cortes e ritmo são adequados sem fórmula repetitiva? |
| Disciplina editorial | Corrigiu o que precisava, deixando o resto em paz? |

Total máximo: 20. Não chame o resultado de “score humano”. Reporte preferências cegas, falhas bloqueantes, média dos avaliadores, dispersão e limitações. O total **não compensa** um erro factual.

## Como documentar resultados

Registre ID do caso, texto de entrada, instrução, versões das skills, modelo e configuração, data, resposta, IDs cegos dos candidatos, notas por critério, bloqueios e justificativa por trecho. Divulgue também os casos perdidos e falhas, não só exemplos vencedores.

## Sinais de regressão

- textos humanos bons sendo reescritos em excesso;
- vocabulário autoral reduzido a “copia premium” neutra;
- dados e qualificações retirados em nome da fluência;
- tudo terminando com uma frase de efeito;
- todas as respostas ganhando subtítulos, bullets ou três itens;
- instruções ou trechos de materiais copiados como se fossem resposta final;
- aumento de falsos positivos dos scripts;
- diagnóstico tratado como prova de autoria.

Sempre corrija regressões sem introduzir novas proibições globais.
