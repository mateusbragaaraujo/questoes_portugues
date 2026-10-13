"""Rodada de treino: sorteio sem repetição e pontuação."""

from __future__ import annotations

import random
from typing import Sequence

TAMANHO_RODADA = 10


class RodadaEncerrada(RuntimeError):
    """A questão atual já foi respondida ou a rodada não avançou."""


class Sessao:
    def __init__(
        self,
        questoes: Sequence[dict],
        tamanho: int = TAMANHO_RODADA,
        gerador: random.Random | None = None,
    ) -> None:
        if tamanho < 1:
            raise ValueError("A rodada precisa ter ao menos uma questão")
        if len(questoes) < tamanho:
            raise ValueError(
                f"O banco tem {len(questoes)} questões e a rodada pede {tamanho}"
            )
        ids = [questao["id"] for questao in questoes]
        if len(ids) != len(set(ids)):
            raise ValueError("O banco contém ids duplicados")
        self.tamanho = tamanho
        self._gerador = gerador or random.Random()
        self.itens = self._gerador.sample(list(questoes), tamanho)
        self.indice = 0
        self.acertos = 0
        self.respondida = False
        self.ultimo_acerto: bool | None = None

    def atual(self) -> dict:
        return self.itens[self.indice]

    def responder(self, usuario_diz_que_esta_correta: bool) -> bool:
        if self.respondida:
            raise RodadaEncerrada("Esta questão já foi respondida")
        acertou = bool(usuario_diz_que_esta_correta) == bool(self.atual()["correta"])
        if acertou:
            self.acertos += 1
        self.respondida = True
        self.ultimo_acerto = acertou
        return acertou

    def avancar(self) -> bool:
        """Vai para a próxima questão. Devolve False quando a rodada acabou."""
        if not self.respondida:
            raise RodadaEncerrada("Responda a questão antes de avançar")
        if self.indice + 1 >= self.tamanho:
            return False
        self.indice += 1
        self.respondida = False
        self.ultimo_acerto = None
        return True

    @property
    def numero(self) -> int:
        return self.indice + 1

    @property
    def acabou(self) -> bool:
        return self.respondida and self.indice == self.tamanho - 1

    def pontuacao(self) -> tuple[int, int]:
        return self.acertos, self.tamanho

    def ids_sorteados(self) -> list[str]:
        return [item["id"] for item in self.itens]
