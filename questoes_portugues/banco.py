"""Leitura do banco de questões."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CAMPOS_OBRIGATORIOS = ("id", "frase", "destaque", "correta", "explicacao", "regra", "fonte")
TEMAS = ("crase", "hifen", "sintaxe")
MINIMO_POR_TEMA = 60


def diretorio_banco() -> Path:
    """Pasta `banco/`, também quando o programa está empacotado."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS")) / "banco"
    return Path(__file__).resolve().parent.parent / "banco"


def carregar_tema(tema: str, diretorio: Path | None = None) -> list[dict]:
    if tema not in TEMAS:
        raise KeyError(f"Tema desconhecido: {tema}")
    pasta = diretorio or diretorio_banco()
    caminho = pasta / f"{tema}.json"
    with caminho.open(encoding="utf-8") as arquivo:
        documento = json.load(arquivo)
    questoes = documento["questoes"]
    if not isinstance(questoes, list):
        raise ValueError(f"{caminho.name}: 'questoes' deve ser uma lista")
    return questoes


def carregar_tudo(diretorio: Path | None = None) -> dict[str, list[dict]]:
    return {tema: carregar_tema(tema, diretorio) for tema in TEMAS}


def validar_questao(questao: dict, indice: int, tema: str) -> list[str]:
    erros: list[str] = []
    prefixo = f"{tema}[{indice}]"
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in questao:
            erros.append(f"{prefixo}: falta o campo '{campo}'")
    if erros:
        return erros

    identificador = questao["id"]
    if not isinstance(identificador, str) or not identificador.strip():
        erros.append(f"{prefixo}: id vazio")
    frase = questao["frase"]
    destaque = questao["destaque"]
    if not isinstance(frase, str) or not frase.strip():
        erros.append(f"{prefixo}: frase vazia")
    if not isinstance(destaque, str) or not destaque.strip():
        erros.append(f"{prefixo}: destaque vazio")
    elif isinstance(frase, str) and destaque not in frase:
        erros.append(f"{prefixo}: destaque não aparece na frase ({identificador})")
    elif isinstance(frase, str) and frase.count(destaque) != 1:
        erros.append(f"{prefixo}: destaque precisa ocorrer uma única vez ({identificador})")
    if not isinstance(questao["correta"], bool):
        erros.append(f"{prefixo}: 'correta' deve ser verdadeiro ou falso")
    for campo in ("explicacao", "regra", "fonte"):
        valor = questao[campo]
        if not isinstance(valor, str) or not valor.strip():
            erros.append(f"{prefixo}: '{campo}' vazio")
    fonte = questao.get("fonte")
    if isinstance(fonte, str) and "http" not in fonte:
        erros.append(f"{prefixo}: fonte sem URL ({identificador})")
    return erros


def validar_banco(banco: dict[str, list[dict]]) -> list[str]:
    erros: list[str] = []
    for tema in TEMAS:
        questoes = banco.get(tema)
        if not isinstance(questoes, list):
            erros.append(f"{tema}: banco ausente")
            continue
        if len(questoes) < MINIMO_POR_TEMA:
            erros.append(f"{tema}: há {len(questoes)} itens; o mínimo é {MINIMO_POR_TEMA}")
        ids: set[str] = set()
        frases: set[str] = set()
        certos = 0
        for indice, questao in enumerate(questoes):
            erros.extend(validar_questao(questao, indice, tema))
            identificador = questao.get("id")
            if isinstance(identificador, str):
                if identificador in ids:
                    erros.append(f"{tema}: id duplicado '{identificador}'")
                ids.add(identificador)
            frase = questao.get("frase")
            if isinstance(frase, str):
                chave = " ".join(frase.split())
                if chave in frases:
                    erros.append(f"{tema}: frase duplicada '{chave[:80]}'")
                frases.add(chave)
            if questao.get("correta") is True:
                certos += 1
        errados = len(questoes) - certos
        if certos < 25 or errados < 25:
            erros.append(f"{tema}: desequilíbrio entre certos ({certos}) e errados ({errados})")
    return erros
