# Ferramentas locais e opcionais

Requerem Python 3.10 ou superior e usam apenas bibliotecas padrão. Não enviam texto para rede, não escrevem nos arquivos originais e não detectam autoria. São alertas para revisão humana, não corretores automáticos.

## Revisão de trechos

~~~bash
python scripts/lint.py documento.txt
python scripts/lint.py documento.md --lang pt --json
cat documento.txt | python scripts/lint.py -
~~~

Ignora blocos de código com cercas, frontmatter, títulos, citações em bloco, links, trechos de código inline e passagens entre aspas delimitadas. A lista de regras é deliberadamente pequena e os alertas podem ter falsos positivos.

## Proteção de dados literais

~~~bash
python scripts/preserve.py original.txt revisado.txt
python scripts/preserve.py original.txt revisado.txt --json --strict
~~~

Compara URLs, e-mails, trechos de código inline, datas numéricas, CPF/CNPJ formatados, moedas, porcentagens, endereços IPv4 e outros números. Diferenças precisam ser inspecionadas; a ferramenta não sabe se duas grafias de uma data são equivalentes, se a troca de unidade é válida ou se o sujeito de uma frase mudou.

Com --strict, lint sai com código 1 para alertas de severidade alta; preserve sai com código 1 para qualquer diferença detectada. Os códigos não são diagnósticos de IA.

## Testes

~~~bash
python -m unittest discover -s tests -v
~~~

Os testes cobrem padrões presentes, exemplos que não devem produzir alertas e comparações conservadoras. A avaliação completa da qualidade editorial está em [benchmark-editorial](../eval/benchmark-editorial.md).
