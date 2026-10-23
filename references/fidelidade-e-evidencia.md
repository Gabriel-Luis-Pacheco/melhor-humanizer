# Fidelidade, evidência e edição de artefatos

Humanização é uma operação semântica conservadora. A revisão pode alterar ordem, fluidez e concisão, mas não o que o material prova, exige ou limita.

## Âncoras que precisam sobreviver

Antes de alterar, confira:
- Pessoas, empresas, produtos, órgãos, locais e nomes próprios.
- Datas, fusos, períodos, competências, quantidades, preços, percentuais, medidas e unidades.
- URLs, endereços, e-mails, caminhos, comandos, identificadores, códigos, fórmulas, rótulos e citações.
- Afirmações negativas e suas exceções.
- Escopo: um, alguns, todos, somente, sempre, nunca.
- Modalidade: pode, poderá, deve, deveria, precisa, recomenda-se, é obrigatório.
- Estado: planejado, em execução, concluído, verificado, aprovado, publicado, disponível em produção.
- Causalidade: “aconteceu após” não vira “foi causado por”.
- Evidência: citado, observado, inferido, estimado ou desconhecido.
- Responsabilidade: quem executou, autorizou ou confirmou.

## Pares de frases que não são equivalentes

- “Pode reduzir o custo” ≠ “reduz o custo”.
- “Será testado” ≠ “foi testado”.
- “Foi implantado” ≠ “funciona em produção”.
- “O problema pode estar no DNS” ≠ “o DNS causou o problema”.
- “A planilha aponta diferença” ≠ “o erro fiscal foi confirmado”.
- “Algumas redes estavam abertas” ≠ “todas as redes estavam abertas”.
- “Deve informar a equipe” ≠ “pode informar a equipe”.
- “A equipe relatou melhora” ≠ “houve melhora comprovada”.

Se uma frase ficou mais curta mas mudou qualquer um desses pontos, volte atrás.

## Proteção de documentos e código

Ao editar um arquivo, identifique sua finalidade e o pedido exato. Mantenha estrutura original salvo instrução contrária. Em planilhas, preserve ordem e significado de colunas, fórmulas, estilos funcionais, dados e abas. Em documentos, preserve citações, bibliografia, figuras, numeração e seções obrigatórias. Em software, não altere código ou configuração por causa de um pedido de humanização de texto.

Nunca substituir código, JSON, YAML, CSV, valores de célula, SQL, logs ou comandos por sinônimos. Se houver textos de interface dentro de um programa, altere só strings autorizadas e confira que placeholders, chaves e quebras funcionais continuam válidos.

## Como lidar com lacunas

Dado essencial ausente: pergunte apenas se a tarefa não puder prosseguir corretamente. Caso contrário, escreva menos e não fabrique. Para relatórios, não finja que foram feitas entrevistas, medições, testes ou verificações. Se o usuário pediu um documento parcial, entregue a parte sustentada pelo material. Se pediu alteração de texto, não acrescente observações meta dentro do documento.

## Verificação final de equivalência

Compare original e revisão em três camadas:
1. **Literal:** nomes, números, datas, URLs, códigos e referências não sumiram nem mudaram?
2. **Lógica:** negações, escopo, incertezas, obrigações, causa, status e sequência estão iguais?
3. **Pragmática:** o texto ainda pede, afirma, critica, admite ou recomenda a mesma coisa no mesmo grau?

O script de preservação verifica apenas uma parte da camada literal. Nada automatizado nesta skill verifica equivalência semântica completa.
