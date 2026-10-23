# Melhor Humanizer

Skill de escrita e revisão pensada primeiro para português brasileiro. Ela corta linguagem artificial, repetição, estruturas de chatbot e exageros, mas não muda os fatos nem força um “jeito humano” genérico.

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

A skill escolhe entre criar, editar, refazer, auditar, adaptar e revisar arquivos. Em seguida, identifica o público e a finalidade, protege dados que não podem mudar, corrige padrões que realmente prejudiquem a leitura e compara significado antes e depois. Ela não mede “quanto o texto é humano” e não promete enganar detectores de IA.

Documentos escolares, acadêmicos, fiscais e técnicos recebem cuidados extras: um texto mais fluido nunca justifica inventar uma medição, uma fonte ou um resultado.

## Arquivos

- [SKILL.md](SKILL.md): instruções principais e regras de decisão.
- [diagnostico.md](references/diagnostico.md): pistas de escrita genérica com exemplos e falsos positivos.
- [voz-e-generos.md](references/voz-e-generos.md): tom adequado para cada tipo de comunicação.
- [fidelidade-e-evidencia.md](references/fidelidade-e-evidencia.md): preservação de fatos, estados, obrigações e artefatos.
- [exemplos.md](references/exemplos.md): exemplos de edição e de quando não editar.
- [fontes-analisadas.md](references/fontes-analisadas.md): comparação documentada de projetos públicos.
- [benchmark-editorial.md](eval/benchmark-editorial.md): avaliação com casos de controle e invariantes.
- [scripts/README.md](scripts/README.md): ferramentas locais opcionais de diagnóstico.

## Diferenças de projeto

Esta skill não proíbe todas as palavras de uma lista, não coloca gíria artificial, não converte todo conteúdo em tópicos e não impõe três passos a qualquer tarefa. O foco é um editor criterioso que também sabe deixar o texto em paz.

O projeto foi concebido com pesquisa em skills públicas e documentação da Wikipedia, com conteúdo original e atribuições em [fontes-analisadas.md](references/fontes-analisadas.md).

## Licença

MIT. Consulte [LICENSE](LICENSE).
