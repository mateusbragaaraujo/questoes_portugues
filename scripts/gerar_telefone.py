"""Gera a página única para abrir no Chrome do celular.

O arquivo leva o banco dentro dele. O Chrome do Android não carrega JSON
ao lado quando a página é aberta de Download.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from questoes_portugues.banco import TEMAS, carregar_tema

DESTINO = RAIZ / "telefone" / "questoes-portugues" / "index.html"

PAGINA = """\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>Questões de Português</title>
<style>
  :root {
    color-scheme: light;
    --fundo: #f4efe4;
    --cartao: #fffdf8;
    --tinta: #1f1a17;
    --mudo: #5e564e;
    --azul: #1e3a5f;
    --azul-ativo: #16304f;
    --contorno: #d9cbb8;
    --destaque: #f6d56b;
    --acerto-fundo: #e5f6ea;
    --acerto-tinta: #14532d;
    --erro-fundo: #fde8e8;
    --erro-tinta: #991b1b;
    --branco: #ffffff;
    --errado: #7f1d1d;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; }
  body {
    background: var(--fundo);
    color: var(--tinta);
    font-family: "Segoe UI", Roboto, system-ui, sans-serif;
    font-size: 17px;
    line-height: 1.45;
  }
  .moldura {
    max-width: 640px;
    margin: 0 auto;
    min-height: 100dvh;
    padding: 24px 16px calc(24px + env(safe-area-inset-bottom));
  }
  h1 {
    font-size: 1.7rem;
    line-height: 1.2;
    margin: 0 0 8px;
  }
  .mudo { color: var(--mudo); }
  .azul { color: var(--azul); font-weight: 700; }
  button {
    font: inherit;
    font-weight: 700;
    border: 0;
    border-radius: 12px;
    min-height: 52px;
    padding: 12px 16px;
    cursor: pointer;
  }
  button:active { transform: translateY(1px); }
  button:disabled { cursor: default; transform: none; opacity: 0.55; }
  button[hidden] { display: none !important; }
  .tema, .primario {
    display: block;
    width: 100%;
    background: var(--azul);
    color: var(--branco);
    margin: 0 0 10px;
  }
  .tema:active, .primario:active { background: var(--azul-ativo); }
  .secundario {
    display: block;
    width: 100%;
    background: var(--cartao);
    color: var(--azul);
    border: 1px solid var(--contorno);
  }
  .topo {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 16px;
  }
  .topo button {
    min-height: 40px;
    background: transparent;
    color: var(--mudo);
    font-weight: 600;
    padding: 8px 4px;
  }
  .frase {
    font-family: Georgia, "Noto Serif", "Times New Roman", serif;
    font-size: 1.35rem;
    line-height: 1.45;
    background: var(--cartao);
    border: 1px solid var(--contorno);
    border-radius: 16px;
    padding: 18px 16px;
    margin: 0;
  }
  mark {
    background: var(--destaque);
    color: inherit;
    font-weight: 700;
    padding: 0 0.12em;
    border-radius: 3px;
  }
  .pergunta { color: var(--mudo); margin: 16px 0 8px; }
  .par {
    display: flex;
    gap: 10px;
  }
  .par button { flex: 1; color: var(--branco); }
  .certo { background: var(--azul); }
  .errado { background: var(--errado); }
  .feedback {
    margin-top: 16px;
    border-radius: 16px;
    padding: 14px 14px 8px;
  }
  .feedback p { margin: 0; }
  .feedback .titulo { font-weight: 700; margin-bottom: 2px; }
  .caixa {
    background: var(--cartao);
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
  }
  .regra { color: var(--azul); font-weight: 700; margin-top: 8px; }
  .fonte { color: var(--mudo); font-size: 0.92rem; margin-top: 8px; overflow-wrap: anywhere; }
  a { color: var(--azul); }
  .rodape { margin-top: 16px; }
  .pontos {
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1;
    margin: 8px 0 12px;
    text-align: center;
  }
  .centro { text-align: center; }
  .pilha { display: flex; flex-direction: column; gap: 10px; margin-top: 8px; }
</style>
</head>
<body>
<main class="moldura" id="tela"></main>
<script id="banco" type="application/json">__BANCO__</script>
<script>
const BANCO = JSON.parse(document.getElementById("banco").textContent);
const TITULOS = { crase: "Crase", hifen: "Hífen", sintaxe: "Análise sintática" };
const TAMANHO = 10;
const tela = document.getElementById("tela");

let tema = null;
let itens = [];
let indice = 0;
let acertos = 0;
let respondida = false;

function embaralhar(lista) {
  const copia = lista.slice();
  for (let i = copia.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    const item = copia[i];
    copia[i] = copia[j];
    copia[j] = item;
  }
  return copia.slice(0, TAMANHO);
}

function limpar(pai) {
  while (pai.firstChild) pai.removeChild(pai.firstChild);
}

function texto(pai, valor, classe) {
  const no = document.createElement(classe === "h1" ? "h1" : "p");
  if (classe && classe !== "h1") no.className = classe;
  no.textContent = valor;
  pai.appendChild(no);
  return no;
}

function botao(pai, rotulo, classe, acao) {
  const no = document.createElement("button");
  no.type = "button";
  no.className = classe;
  no.textContent = rotulo;
  no.addEventListener("click", acao);
  pai.appendChild(no);
  return no;
}

function comentario(pontos, total) {
  if (pontos === total) return "Dez em dez. A rodada fechou sem erro.";
  if (pontos >= 7) return "Bom resultado. Dá para firmar o que ainda oscilou jogando de novo.";
  if (pontos >= 5) return "Metade ou um pouco mais. Vale repetir o tema com outras frases.";
  return "A rodada mostrou o que revisar. A explicação de cada item continua no banco.";
}

function escreverFrase(pai, frase, destaque) {
  const no = document.createElement("p");
  no.className = "frase";
  const inicio = frase.indexOf(destaque);
  if (inicio < 0) {
    no.textContent = frase;
  } else {
    no.appendChild(document.createTextNode(frase.slice(0, inicio)));
    const marca = document.createElement("mark");
    marca.textContent = destaque;
    no.appendChild(marca);
    no.appendChild(document.createTextNode(frase.slice(inicio + destaque.length)));
  }
  pai.appendChild(no);
}

function escreverFonte(pai, fonte) {
  const no = document.createElement("p");
  no.className = "fonte";
  fonte.split(/(https?:\\/\\/[^\\s]+)/).forEach(function (pedaco) {
    if (!/^https?:\\/\\//.test(pedaco)) {
      no.appendChild(document.createTextNode(pedaco));
      return;
    }
    let url = pedaco;
    let resto = "";
    const corte = url.match(/[)\\].,;:]+$/);
    if (corte) {
      resto = corte[0];
      url = url.slice(0, -resto.length);
    }
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = url;
    no.appendChild(link);
    if (resto) no.appendChild(document.createTextNode(resto));
  });
  pai.appendChild(no);
}

function mostrarMenu() {
  tema = null;
  itens = [];
  limpar(tela);
  texto(tela, "Questões de Português", "h1");
  texto(tela, "Treino de crase, de hífen e de análise sintática com frases de prova. Dez questões por rodada, sem repetir.", "mudo");
  botao(tela, "Crase", "tema", function () { iniciar("crase"); });
  botao(tela, "Hífen", "tema", function () { iniciar("hifen"); });
  botao(tela, "Análise sintática", "tema", function () { iniciar("sintaxe"); });
  texto(tela, "Escolha um tema. Em cada frase, o trecho em destaque está certo ou errado.", "mudo");
  window.scrollTo(0, 0);
}

function iniciar(novoTema) {
  tema = novoTema;
  itens = embaralhar(BANCO[novoTema]);
  indice = 0;
  acertos = 0;
  respondida = false;
  mostrarQuestao();
}

function mostrarQuestao() {
  const questao = itens[indice];
  limpar(tela);
  const topo = document.createElement("div");
  topo.className = "topo";
  const progresso = document.createElement("p");
  progresso.className = "azul";
  progresso.textContent = TITULOS[tema] + "  ·  questão " + (indice + 1) + " de " + TAMANHO;
  topo.appendChild(progresso);
  botao(topo, "Menu", "", function () {
    if (window.confirm("Abandonar esta rodada e voltar ao menu?")) mostrarMenu();
  });
  tela.appendChild(topo);
  escreverFrase(tela, questao.frase, questao.destaque);
  texto(
    tela,
    tema === "sintaxe"
      ? "A classificação destacada está correta?"
      : "O trecho em destaque está de acordo com a norma?",
    "pergunta"
  );
  const par = document.createElement("div");
  par.className = "par";
  const certo = botao(par, "Certo", "certo", function () { responder(true); });
  const errado = botao(par, "Errado", "errado", function () { responder(false); });
  tela.appendChild(par);
  const faixa = document.createElement("div");
  tela.appendChild(faixa);
  const rodape = document.createElement("div");
  rodape.className = "rodape";
  const proxima = botao(rodape, indice === TAMANHO - 1 ? "Ver pontuação" : "Próxima", "primario", avancar);
  proxima.disabled = true;
  proxima.hidden = true;
  tela.appendChild(rodape);

  function responder(usuarioDizQueEstaCorreta) {
    if (respondida) return;
    respondida = true;
    const acertou = usuarioDizQueEstaCorreta === questao.correta;
    if (acertou) acertos += 1;
    certo.disabled = true;
    errado.disabled = true;
    const painel = document.createElement("div");
    painel.className = "feedback";
    painel.style.background = acertou ? "var(--acerto-fundo)" : "var(--erro-fundo)";
    const titulo = document.createElement("p");
    titulo.className = "titulo";
    titulo.style.color = acertou ? "var(--acerto-tinta)" : "var(--erro-tinta)";
    titulo.textContent = acertou ? "Você acertou." : "Você errou.";
    painel.appendChild(titulo);
    const julgamento = document.createElement("p");
    if (tema === "sintaxe") {
      julgamento.textContent = "Pela análise da prova, esta classificação está " + (questao.correta ? "certa." : "errada.");
    } else {
      julgamento.textContent = "Pela norma, este emprego está " + (questao.correta ? "certo." : "errado.");
    }
    painel.appendChild(julgamento);
    const caixa = document.createElement("div");
    caixa.className = "caixa";
    texto(caixa, questao.explicacao, "");
    const regra = texto(caixa, questao.regra, "regra");
    regra.style.marginTop = "8px";
    escreverFonte(caixa, questao.fonte);
    painel.appendChild(caixa);
    faixa.appendChild(painel);
    proxima.hidden = false;
    proxima.disabled = false;
    proxima.textContent = indice === TAMANHO - 1 ? "Ver pontuação" : "Próxima";
    painel.scrollIntoView({ block: "nearest" });
  }

  window.scrollTo(0, 0);
}

function avancar() {
  if (!respondida) return;
  if (indice + 1 >= TAMANHO) {
    mostrarResultado();
    return;
  }
  indice += 1;
  respondida = false;
  mostrarQuestao();
}

function mostrarResultado() {
  limpar(tela);
  texto(tela, TITULOS[tema], "azul centro");
  texto(tela, "Pontuação", "mudo centro");
  const pontos = document.createElement("p");
  pontos.className = "pontos";
  pontos.textContent = acertos + "/" + TAMANHO;
  tela.appendChild(pontos);
  const nota = texto(tela, comentario(acertos, TAMANHO), "mudo centro");
  nota.style.marginBottom = "20px";
  const pilha = document.createElement("div");
  pilha.className = "pilha";
  botao(pilha, "Jogar de novo", "primario", function () { iniciar(tema); });
  botao(pilha, "Voltar ao menu", "secundario", mostrarMenu);
  tela.appendChild(pilha);
  window.scrollTo(0, 0);
}

mostrarMenu();
</script>
</body>
</html>
"""


def gerar(destino: Path = DESTINO) -> Path:
    banco = {tema: carregar_tema(tema) for tema in TEMAS}
    payload = json.dumps(banco, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(PAGINA.replace("__BANCO__", payload), encoding="utf-8")
    return destino


if __name__ == "__main__":
    caminho = gerar()
    print(caminho)
