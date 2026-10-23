# Benchmark editorial da Melhor Humanizer

Este documento define **como avaliar**, não anuncia um resultado que ainda não foi medido. Nenhuma nota de um detector de autoria substitui avaliação de leitura, preservação de fatos e respeito à intenção do autor.

## Método recomendado

Para comparar versões, ofereça a avaliadores os mesmos textos e pedidos, sem revelar qual skill gerou qual edição. Embaralhe a ordem. Avalie em português brasileiro, com públicos e gêneros diversos. Inclua controles humanos de boa qualidade e textos difíceis em que a melhor revisão é nenhuma.

Cada caso recebe julgamento **aprovado/reprovado** em invariantes:
1. Não criou, apagou ou alterou fatos ou requisitos relevantes.
2. Preservou incerteza, modalidade, escopo, negação, causalidade e estado.
3. Respeitou a voz fornecida e o gênero.
4. Deu ao leitor a informação necessária com clareza e sem inflação.
5. Não introduziu estruturas artificiais, slogans genéricos ou reformatações supérfluas.
6. Não editou artefatos fora do escopo.
7. Não alegou ter identificado com certeza a autoria por IA nem prometeu evasão de detector.

Além desses critérios obrigatórios, peça preferência de leitura cega e justificativa concreta. Uma versão que viola (1), (2) ou (6) não deve vencer por “soar mais natural”.

## Casos manuais adversariais

| ID | Entrada/solicitação | Invariante de aprovação |
| --- | --- | --- |
| 01 | “Humaniza: É importante ressaltar que o relatório está disponível.” | Evitar abertura vazia; preservar disponibilidade. |
| 02 | “Revisa: Pode haver divergência, mas não fizemos teste.” | Conservar hipótese e ausência de teste. |
| 03 | “Bah, eu tentei e não rolou kkk” | Não formalizar nem inserir falsa erudição. |
| 04 | “O endpoint retorna 409 se a chave já existe.” | Manter status HTTP e condição, sem inventar mecanismo. |
| 05 | “1. Acesse 2. Confirme 3. Envie” | Manter ordem necessária, apesar de serem três itens. |
| 06 | “Houve melhora de 12%, segundo a empresa.” | Conservar número e atribuição; não afirmar comprovação independente. |
| 07 | “O sistema deverá ser publicado amanhã.” | Não converter intenção futura em publicação concluída. |
| 08 | “Não foi possível concluir a análise.” | Não inverter negação nem apagar o limite. |
| 09 | “Preciso de relatório com seções 1, 2 e 3.” | Preservar estrutura obrigatória; sem novas seções. |
| 10 | “Reescreva minha mensagem: te amo mttt ❤️” | Preservar intimidade e registro escolhido. |
| 11 | “Melhore a LP, não invente funcionalidades.” | Sem recursos, métricas ou provas sociais não fornecidos. |
| 12 | “Revise esta citação e mantenha as aspas” | Conteúdo e atribuição da citação idênticos. |
| 13 | “Faça mais simples sem mexer no CNPJ 12.345.678/0001-90.” | Identificador idêntico. |
| 14 | “A implantação terminou; ainda não testamos produção.” | Manter implantação e verificação como estados separados. |
| 15 | “Deixa esse documento mais natural; não altere planilha anexa.” | Nenhum campo, aba, fórmula ou estilo funcional modificado. |
| 16 | “Troque 'a grande revolução' por algo claro, sem contexto extra.” | Corrigir exagero sem inventar característica. |
| 17 | “Audita somente, sem editar.” | Reportar problemas específicos sem produzir versão revisada. |
| 18 | “Humaniza: O céu estava azul naquele dia.” | Deixar frase boa em paz. |

## Controles para detectar over-edit

Inclua pelo menos um terço de exemplos humanos ou tecnicamente corretos que não devem ser retocados por preferência estética. Compare a quantidade de mudanças com a quantidade de problemas reais resolvidos. Exemplos com voz informal, passiva justificada, gerúndio funcional, três elementos reais e travessões intencionais devem ser preservados.

## Testes automáticos

Os comandos disponíveis na pasta scripts são alertas auxiliares. Os testes de unidade são verificações da ferramenta, não testes cegos de qualidade da skill. Quando resultados de avaliação real forem produzidos, registre corpus, versões, avaliadores, decisões, erros, falsos positivos e limites, sem usar taxa de aprovação inventada.
