# Melhor Humanizer — v2.0

Skill de edição para português brasileiro e inglês. Corrige trechos artificiais sem inventar fatos, alterar requisitos ou apagar a voz do autor. O ponto principal é saber quanto mudar — inclusive quando não mudar nada.

## Para que serve

Humanizar um texto que ficou com cara de IA, melhorar uma redação, reescrever trechos de um relatório, revisar posts, e-mails, roteiros, textos acadêmicos, documentação e microcopy. Também serve para auditar um texto sem mexer nele.

O padrão é **alterar o mínimo necessário**. Isso inclui respeitar a voz do autor, não mudar o significado de palavras técnicas, preservar dados e manter a formatação funcional dos arquivos.

## Instalação

Compatível com ferramentas que suportam o formato aberto Agent Skills. Pela CLI Skills:

~~~bash
npx skills add https://github.com/Gabriel-Luis-Pacheco/melhor-humanizer --skill melhor-humanizer
~~~

Também é possível copiar a pasta do repositório para o diretório de skills do agente, conforme a documentação da ferramenta. A entrada é [SKILL.md](SKILL.md). As referências são carregadas quando necessárias; os scripts são opcionais.

## Exemplos de uso

- “Humaniza esse texto mantendo meu jeito de escrever e sem inventar nada.”
- “Revisa esse relatório e tira a escrita genérica, mas preserva números e termos fiscais.”
- “Deixa esse trabalho escolar mais simples e natural, mantendo o roteiro do professor.”
- “Audita esse texto: aponta repetições e trechos artificiais, sem reescrever.”
- “Cria uma mensagem curta para WhatsApp, sem formalidade nem frases prontas.”
- “Melhora a copy da landing page, mas não inventa funcionalidades.”

## Como funciona

A skill começa pela finalidade e pelos dados do texto, não por uma lista de palavras proibidas. Ela escolhe entre criar, editar, refazer, auditar, adaptar e revisar arquivos, determina o grau de intervenção (nenhum, leve, moderado ou profundo) e respeita uma hierarquia: evidências, restrições do documento, convenções do gênero, voz do autor e preferências estilísticas. Travessões, advérbios, listas e frases curtas só são problema quando prejudicam a leitura.

Ela usa amostras fornecidas para aprender escolhas observáveis da pessoa e não supõe personalidade, origem regional, experiência ou opinião. Ao criar conteúdo novo, privilegia a informação que o leitor precisa em vez de só evitar clichês. Confira [o sistema de decisões](references/decisoes-editoriais.md), [a adaptação de voz](references/perfil-de-voz.md) e [a escrita original](references/escrita-original.md).

A comparação automática sinaliza mudanças em números, URLs, datas, negações, incerteza, obrigações e estados como planejado/testado. **Nenhuma ferramenta local valida sozinha o significado**; os alertas exigem revisão contextual.

Documentos escolares, acadêmicos, fiscais e técnicos recebem cuidados extras: um texto mais fluido nunca justifica inventar uma medição, uma fonte ou um resultado.

## Arquivos

- [SKILL.md](SKILL.md): instruções principais e regras de decisão.
- [diagnostico.md](references/diagnostico.md): pistas de escrita genérica com exemplos e falsos positivos.
- [voz-e-generos.md](references/voz-e-generos.md): tom adequado para cada tipo de comunicação.
- [fidelidade-e-evidencia.md](references/fidelidade-e-evidencia.md): preservação de fatos, estados, obrigações e artefatos.
- [exemplos.md](references/exemplos.md): exemplos de edição e de quando não editar.
- [fontes-analisadas.md](references/fontes-analisadas.md): comparação documentada de projetos públicos.
- [portugues-natural.md](references/portugues-natural.md): particularidades reais do português brasileiro.
- [decisoes-editoriais.md](references/decisoes-editoriais.md): como decidir entre corrigir e preservar.
- [perfil-de-voz.md](references/perfil-de-voz.md): respeito à voz do autor.
- [escrita-original.md](references/escrita-original.md): produzir bom texto novo, não só remover termos.
- [avaliacao-cega.md](eval/avaliacao-cega.md): metodologia comparativa com bloqueios factuais.
- [benchmark-editorial.md](eval/benchmark-editorial.md): avaliação com casos de controle e invariantes.
- [scripts/README.md](scripts/README.md): ferramentas locais opcionais de diagnóstico.

## Testes e comparação de resultados

Os scripts rodam localmente com Python 3.10+ e biblioteca padrão. Não enviam texto para serviço externo nem reescrevem arquivos.

~~~bash
python scripts/lint.py rascunho.md --lang pt
python scripts/preserve.py original.txt revisado.txt --json
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python eval/check_runs.py --validate-corpus
~~~

O [corpus de 40 cenários](eval/casos.jsonl) inclui 16 controles para detectar edição excessiva. Para comparar saídas reais de agentes, prepare um JSONL com campos id, output e candidate opcional e rode python eval/check_runs.py respostas.jsonl --json. Os resultados apontam alertas, **não garantem qualidade ou autoria**. O protocolo de comparação cega está em [avaliação cega](eval/avaliacao-cega.md).

## Diferenças de projeto

Esta skill não proíbe todas as palavras de uma lista, não coloca gíria artificial, não converte todo conteúdo em tópicos e não impõe três passos a qualquer tarefa. O foco é um editor criterioso que também sabe deixar o texto em paz.

O projeto foi concebido com pesquisa em skills públicas e documentação da Wikipedia, com conteúdo original e atribuições em [fontes-analisadas.md](references/fontes-analisadas.md).

## Limites

Esta é uma skill de instruções, não um serviço que reescreve automaticamente, nem uma ferramenta para manipular detectores de autoria. Resultados dependem do modelo, contexto e evidência disponíveis. Não há comprovação de que supere universalmente outras skills sem avaliações cegas executadas.

## Licença

MIT. Consulte [LICENSE](LICENSE).
