"""Fluxo da janela: menu, resposta, pontuação e nova rodada."""

import tkinter as tk

import pytest

from questoes_portugues.app import Aplicativo
from questoes_portugues.banco import carregar_tudo


@pytest.fixture(scope="module")
def raiz():
    """Uma única janela para o módulo.

    No Python do GitHub Actions, o segundo ``Tk()`` do mesmo processo não
    consegue reler o ``init.tcl``.
    """
    janela = tk.Tk()
    janela.withdraw()
    yield janela
    janela.destroy()


def test_fluxo_dos_dois_temas_ate_a_pontuacao(raiz):
    app = Aplicativo(raiz, carregar_tudo())
    assert app.quadro_menu.winfo_manager() == "pack"
    for tema in ("crase", "hifen", "sintaxe"):
        app.iniciar(tema)
        assert app.quadro_questao.winfo_manager() == "pack"
        assert app.quadro_menu.winfo_manager() == ""
        vistos = []
        for numero in range(1, 11):
            assert app.sessao.numero == numero
            vistos.append(app.sessao.atual()["id"])
            app.responder(app.sessao.atual()["correta"])
            assert "Você acertou." in app.rotulo_feedback.cget("text")
            app.proxima()
        assert len(set(vistos)) == 10
        assert app.quadro_resultado.winfo_manager() == "pack"
        assert app.rotulo_pontos.cget("text") == "10/10"
    app.mostrar_menu()
    assert app.quadro_menu.winfo_manager() == "pack"
    assert app.sessao is None


def test_erro_nao_soma_ponto_e_proxima_so_depois_da_resposta(raiz):
    app = Aplicativo(raiz, carregar_tudo())
    app.iniciar("crase")
    app.proxima()
    assert app.sessao.numero == 1
    app.responder(not app.sessao.atual()["correta"])
    assert app.rotulo_feedback.cget("text") == "Você errou."
    assert app.sessao.acertos == 0
    app.responder(True)
    assert app.sessao.acertos == 0
