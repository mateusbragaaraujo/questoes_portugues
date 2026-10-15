"""A página do celular leva o banco inteiro e abre sem arquivo ao lado."""

from pathlib import Path

from questoes_portugues.banco import TEMAS, carregar_tema

PAGINA = Path("telefone/questoes-portugues/index.html")


def test_pagina_e_autonoma_e_traz_cada_questao():
    html = PAGINA.read_text(encoding="utf-8")
    assert html.startswith("<!DOCTYPE html>")
    assert 'src="' not in html
    assert "http://" not in html.split("<script", 1)[0]
    assert "https://" not in html.split("<script", 1)[0]
    for tema in TEMAS:
        for questao in carregar_tema(tema):
            assert questao["id"] in html
            assert questao["destaque"] in html
