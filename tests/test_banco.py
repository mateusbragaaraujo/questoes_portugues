"""Valida o banco publicado: campos, fontes e equilíbrio."""

from questoes_portugues.banco import CAMPOS_OBRIGATORIOS, MINIMO_POR_TEMA, TEMAS, carregar_tudo, validar_banco


def test_banco_publicado_e_valido():
    banco = carregar_tudo()
    assert validar_banco(banco) == []


def test_cada_tema_tem_os_dois_julgamentos():
    banco = carregar_tudo()
    for tema in TEMAS:
        questoes = banco[tema]
        assert len(questoes) >= MINIMO_POR_TEMA
        certos = [questao for questao in questoes if questao["correta"]]
        errados = [questao for questao in questoes if not questao["correta"]]
        assert len(certos) >= 25
        assert len(errados) >= 25


def test_campos_e_fonte_com_url():
    banco = carregar_tudo()
    for tema in TEMAS:
        for questao in banco[tema]:
            for campo in CAMPOS_OBRIGATORIOS:
                assert campo in questao
            assert questao["destaque"] in questao["frase"]
            assert "http" in questao["fonte"]
            assert questao["id"].startswith(tema + "-")
