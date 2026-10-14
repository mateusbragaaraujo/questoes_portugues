# Banco de questões

Cada tema fica num arquivo JSON: `crase.json`, `hifen.json` e `sintaxe.json`. O programa lê a lista `questoes` e sorteia 10 itens sem repetir na rodada.

## O que entra no banco

A frase e o gabarito vêm de questão de prova já publicada (banca, compilação de provas ou página que reproduz o item com o gabarito). A explicação resume a regra citada nessa fonte ou no Acordo Ortográfico, no comentário do professor ou na gramática indicada no campo `fonte`. Item sem fonte não deve ser acrescentado.

Não reescreva a frase para “ficar mais clara”. Se a prova só trouxe a palavra ou a alternativa, use esse texto.

## Campos de cada questão

| Campo | O que é |
| --- | --- |
| `id` | Identificador único no tema, no formato `crase-001`, `hifen-001` ou `sintaxe-001`. |
| `frase` | Texto como está na prova ou na alternativa. |
| `destaque` | Trecho de `frase` que o programa sublinha. Precisa aparecer uma única vez. |
| `correta` | `true` se esse emprego, do jeito que está escrito, está de acordo com a norma; `false` se está errado. O valor segue o gabarito, não uma impressão. |
| `explicacao` | Por que está certo ou errado, em poucas frases. |
| `regra` | Nome curto da regra. |
| `fonte` | Banca, ano, órgão ou cargo, gabarito e um URL. Sem URL o teste recusa o item. |

Exemplo:

```json
{
  "id": "hifen-099",
  "frase": "auto-escola",
  "destaque": "auto-escola",
  "correta": false,
  "explicacao": "A grafia exigida pela prova é autoescola, sem hífen: vogais diferentes se aglutinam.",
  "regra": "Base XVI: vogais diferentes se aglutinam.",
  "fonte": "Gestão de Concursos – 2018 – EMATER-MG. Gabarito: D. https://www.estrategiaconcursos.com.br/curso/main/downloadPDF/?aula=835970"
}
```

## Como incluir uma questão

1. Abra o JSON do tema.
2. Copie um item, dê um `id` novo e preencha os campos com o texto e o gabarito da prova.
3. Confira se `destaque` está dentro de `frase` uma só vez.
4. Rode `pytest`. O teste exige, em cada tema, no mínimo 60 itens, sem `id` ou frase repetidos, com os dois julgamentos (pelo menos 25 certos e 25 errados).

## De onde vieram os itens atuais

- Crase: alternativas de provas reproduzidas no capítulo de crase de *900 questões de gramática aplicada*, de Décio Sena, e questões comentadas de FGV, Cebraspe, FCC, Vunesp, Cesgranrio, IBFC, Quadrix e Avança SP. A regra citada em cada item aponta o comentário ou a gramática usada.
- Hífen: questões de 2018 e 2019 comentadas por Décio Terror (FUNDEP, NC-UFPR, FUNDATEC, IBGP, Funrio, FUMARC, FGV, AOCP, UFRR, FCM e Gestão de Concursos), conferidas com a Base XV e a Base XVI do Acordo Ortográfico de 1990 e, nos compostos aglutinados e nas locuções, com o texto de Evanildo Bechara na ABL.
- Análise sintática: enunciados em que a frase analisada está no próprio item, com gabarito publicado por Avança SP, EEAR, FCC, UFRJ, CETREDE, Vunesp, FEPESE, IADES, Consulplan, Cespe/Cebraspe, FAUEL, IBFC, IESES, IDECAN, FGV, FUNCAB, IBADE, IBEG, Instituto Machado de Assis e MS Concursos. Em análise sintática, `correta` diz se a classificação destacada confere com esse gabarito.
