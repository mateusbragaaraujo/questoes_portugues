"""Pontuação, sorteio sem repetição e fluxo da rodada."""

import random

import pytest

from questoes_portugues.banco import carregar_tudo
from questoes_portugues.sessao import TAMANHO_RODADA, RodadaEncerrada, Sessao


@pytest.fixture
def questoes():
    return carregar_tudo()["crase"]


def test_rodada_tem_dez_itens_sem_repetir(questoes):
    sessao = Sessao(questoes, gerador=random.Random(3))
    ids = sessao.ids_sorteados()
    assert len(ids) == TAMANHO_RODADA
    assert len(set(ids)) == TAMANHO_RODADA
    assert set(ids).issubset({questao["id"] for questao in questoes})


def test_duas_rodadas_podem_diferir(questoes):
    uma = Sessao(questoes, gerador=random.Random(1)).ids_sorteados()
    outra = Sessao(questoes, gerador=random.Random(2)).ids_sorteados()
    assert uma != outra


def test_pontuacao_soma_so_os_acertos(questoes):
    sessao = Sessao(questoes, gerador=random.Random(7))
    esperados = 0
    for indice in range(TAMANHO_RODADA):
        questao = sessao.atual()
        # Alterna: acerta nas pares, erra nas ímpares.
        chute_certo = indice % 2 == 0
        resposta = questao["correta"] if chute_certo else not questao["correta"]
        acertou = sessao.responder(resposta)
        assert acertou is chute_certo
        if chute_certo:
            esperados += 1
        if indice < TAMANHO_RODADA - 1:
            assert sessao.avancar() is True
    assert sessao.acabou
    assert sessao.avancar() is False
    assert sessao.pontuacao() == (esperados, TAMANHO_RODADA)


def test_nao_avanca_nem_responde_duas_vezes(questoes):
    sessao = Sessao(questoes, tamanho=2, gerador=random.Random(0))
    with pytest.raises(RodadaEncerrada):
        sessao.avancar()
    sessao.responder(True)
    with pytest.raises(RodadaEncerrada):
        sessao.responder(False)
    assert sessao.pontuacao()[0] in (0, 1)


def test_banco_curto_nao_monta_rodada():
    with pytest.raises(ValueError):
        Sessao([{"id": "x", "correta": True}], tamanho=10)


def test_hifen_tambem_sorteia_dez():
    questoes = carregar_tudo()["hifen"]
    sessao = Sessao(questoes, gerador=random.Random(11))
    assert len(sessao.ids_sorteados()) == 10
    assert len(set(sessao.ids_sorteados())) == 10
