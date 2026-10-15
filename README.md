# Questões de Português

Programa de desktop para treinar **crase**, **hífen** e **análise sintática** do jeito que a prova cobra: uma frase, o trecho em destaque, e a decisão **Certo** ou **Errado**.

A interface está em português do Brasil. Cada rodada tem 10 questões sorteadas, sem repetir dentro da rodada. No fim aparece a pontuação (por exemplo, 7/10), com a opção de jogar de novo ou voltar ao menu.

As frases e os gabaritos foram tirados de questões de concurso já publicadas. A explicação de cada item cita a regra e a fonte (banca, ano, órgão ou URL). O formato do banco está em [banco/LEIA-ME.md](banco/LEIA-ME.md).

## Rodar no Windows

É preciso o Python 3.11 ou mais novo, com Tcl/Tk. No instalador de [python.org](https://www.python.org/downloads/windows/), marque **tcl/tk and IDLE**.

Na pasta do projeto:

```bat
python main.py
```

Também funciona:

```bat
python -m questoes_portugues
```

Não há bibliotecas para instalar só para jogar. O Tkinter já vem com o Python.

## Como jogar

1. Na tela inicial, escolha **Crase**, **Hífen** ou **Análise sintática**.
2. Leia a frase. O trecho julgado fica marcado em amarelo.
3. Clique em **Certo** ou **Errado** (atalhos `C` e `E`).
4. O programa diz se você acertou, mostra a regra e a fonte. Clique em **Próxima** (ou Enter).
5. Depois da 10.ª questão, aparece a pontuação. **Jogar de novo** sorteia outras 10 do mesmo tema. **Voltar ao menu** troca de tema.

## Testes

```bat
pip install pytest
pytest
```

Os testes conferem o banco (campos obrigatórios, fonte com URL, sem frase nem id repetidos, pelo menos 60 itens por tema, casos certos e errados) e a pontuação da rodada.

## Executável de Windows

O arquivo pronto para duplo clique é [release/QuestoesDePortugues.exe](release/QuestoesDePortugues.exe). Não precisa instalar Python. O banco de questões vai dentro do executável.

Cada envio para o GitHub gera de novo esse arquivo no fluxo **Executavel Windows**. O artefato da execução mais recente fica na aba Actions.

Para gerar na sua máquina, na pasta do projeto:

```bat
scripts\build_exe.bat
```

O script instala o PyInstaller, se ainda não estiver instalado, e gera `dist\QuestoesDePortugues.exe`.

Se o `.exe` abrir e fechar na hora, use `python main.py`. O atalho da área de trabalho não é obrigatório.

## Incluir questões

Edite `banco/crase.json`, `banco/hifen.json` ou `banco/sintaxe.json`. Cada item precisa de frase, trecho em destaque, gabarito (`correta`: verdadeiro ou falso), explicação, regra e fonte com URL. O passo a passo está em [banco/LEIA-ME.md](banco/LEIA-ME.md).
