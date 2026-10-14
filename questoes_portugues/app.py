"""Interface de treino em português do Brasil."""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

from questoes_portugues.banco import carregar_tudo
from questoes_portugues.sessao import Sessao, RodadaEncerrada

TITULOS = {
    "crase": "Crase",
    "hifen": "Hífen",
    "sintaxe": "Análise sintática",
}

CORES = {
    "fundo": "#f4efe4",
    "cartao": "#fffdf8",
    "tinta": "#1f1a17",
    "mudo": "#5e564e",
    "azul": "#1e3a5f",
    "azul_ativo": "#16304f",
    "contorno": "#d9cbb8",
    "destaque": "#f6d56b",
    "acerto_fundo": "#e5f6ea",
    "acerto_tinta": "#14532d",
    "erro_fundo": "#fde8e8",
    "erro_tinta": "#991b1b",
    "branco": "#ffffff",
}


def _primeira_fonte(raiz: tk.Misc, candidatas: tuple[str, ...], tamanho: int, peso: str = "normal") -> tuple:
    disponiveis = {nome.lower() for nome in tkfont.families(raiz)}
    for nome in candidatas:
        if nome.lower() in disponiveis:
            return (nome, tamanho, peso)
    return ("TkDefaultFont", tamanho, peso)


class Aplicativo:
    def __init__(self, raiz: tk.Tk, banco: dict | None = None) -> None:
        self.raiz = raiz
        self.banco = banco if banco is not None else carregar_tudo()
        self.tema: str | None = None
        self.sessao: Sessao | None = None

        self.fonte_titulo = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 26, "bold")
        self.fonte_ui = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 13)
        self.fonte_ui_bold = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 13, "bold")
        self.fonte_botao = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 15, "bold")
        self.fonte_frase = _primeira_fonte(raiz, ("Georgia", "Liberation Serif", "DejaVu Serif"), 20)
        self.fonte_miuda = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 11)
        self.fonte_pontos = _primeira_fonte(raiz, ("Segoe UI", "DejaVu Sans", "Noto Sans"), 42, "bold")

        raiz.title("Questões de Português")
        raiz.configure(bg=CORES["fundo"])
        raiz.minsize(720, 560)
        raiz.geometry("880x680")

        self.conteudo = tk.Frame(raiz, bg=CORES["fundo"])
        self.conteudo.pack(fill="both", expand=True)

        self._montar_menu()
        self._montar_questao()
        self._montar_resultado()
        self.mostrar_menu()

        raiz.bind("<c>", lambda _e: self._atalho_resposta(True))
        raiz.bind("<C>", lambda _e: self._atalho_resposta(True))
        raiz.bind("<e>", lambda _e: self._atalho_resposta(False))
        raiz.bind("<E>", lambda _e: self._atalho_resposta(False))
        raiz.bind("<Return>", lambda _e: self._atalho_avancar())

    def _limpar(self) -> None:
        for quadro in (self.quadro_menu, self.quadro_questao, self.quadro_resultado):
            quadro.pack_forget()

    def mostrar_menu(self) -> None:
        self.tema = None
        self.sessao = None
        self._limpar()
        self.quadro_menu.pack(fill="both", expand=True)

    def iniciar(self, tema: str) -> None:
        self.tema = tema
        self.sessao = Sessao(self.banco[tema])
        self._limpar()
        self.quadro_questao.pack(fill="both", expand=True)
        self._mostrar_questao()

    def responder(self, usuario_diz_que_esta_correta: bool) -> None:
        if self.sessao is None:
            return
        try:
            acertou = self.sessao.responder(usuario_diz_que_esta_correta)
        except RodadaEncerrada:
            return
        questao = self.sessao.atual()
        if acertou:
            self.painel_feedback.configure(bg=CORES["acerto_fundo"])
            self.rotulo_feedback.configure(
                text="Você acertou.",
                bg=CORES["acerto_fundo"],
                fg=CORES["acerto_tinta"],
            )
        else:
            self.painel_feedback.configure(bg=CORES["erro_fundo"])
            self.rotulo_feedback.configure(
                text="Você errou.",
                bg=CORES["erro_fundo"],
                fg=CORES["erro_tinta"],
            )
        if self.tema == "sintaxe":
            estado = "certa" if questao["correta"] else "errada"
            texto_julgamento = f"Pela análise da prova, esta classificação está {estado}."
        else:
            julgamento = "certo" if questao["correta"] else "errado"
            texto_julgamento = f"Pela norma, este emprego está {julgamento}."
        self.rotulo_julgamento.configure(
            text=texto_julgamento,
            bg=self.painel_feedback.cget("bg"),
            fg=CORES["tinta"],
        )
        self.rotulo_explicacao.configure(text=questao["explicacao"])
        self.rotulo_regra.configure(text=questao["regra"])
        self.rotulo_fonte.configure(text=questao["fonte"])
        self.faixa_feedback.pack(fill="both", expand=True, pady=(12, 0))
        self.canvas_feedback.yview_moveto(0)
        self._sincronizar_rolagem()
        self.botao_certo.configure(state="disabled")
        self.botao_errado.configure(state="disabled")
        texto_proxima = "Ver pontuação" if self.sessao.acabou else "Próxima"
        self._estado_proxima(True, texto_proxima)

    def proxima(self) -> None:
        if self.sessao is None:
            return
        try:
            ainda_ha = self.sessao.avancar()
        except RodadaEncerrada:
            return
        if ainda_ha:
            self._mostrar_questao()
        else:
            self._mostrar_resultado()

    def _mostrar_questao(self) -> None:
        assert self.sessao is not None and self.tema is not None
        questao = self.sessao.atual()
        titulo = TITULOS.get(self.tema, self.tema)
        self.rotulo_progresso.configure(
            text=f"{titulo}  ·  questão {self.sessao.numero} de {self.sessao.tamanho}"
        )
        if self.tema == "sintaxe":
            pergunta = "A classificação destacada está correta?"
        else:
            pergunta = "O trecho em destaque está de acordo com a norma?"
        self.rotulo_pergunta.configure(text=pergunta)
        self._escrever_frase(questao["frase"], questao["destaque"])
        self.faixa_feedback.pack_forget()
        self.botao_certo.configure(state="normal")
        self.botao_errado.configure(state="normal")
        self._estado_proxima(False, "Próxima")

    def _escrever_frase(self, frase: str, destaque: str) -> None:
        texto = self.texto_frase
        texto.configure(state="normal")
        texto.delete("1.0", "end")
        inicio = frase.index(destaque)
        fim = inicio + len(destaque)
        texto.insert("1.0", frase[:inicio])
        texto.insert("end", destaque, "destaque")
        texto.insert("end", frase[fim:])
        linhas = max(3, min(8, len(frase) // 48 + 1))
        texto.configure(state="disabled", height=linhas)

    def _mostrar_resultado(self) -> None:
        assert self.sessao is not None and self.tema is not None
        acertos, total = self.sessao.pontuacao()
        self._limpar()
        self.quadro_resultado.pack(fill="both", expand=True)
        titulo = TITULOS.get(self.tema, self.tema)
        self.rotulo_tema_final.configure(text=titulo)
        self.rotulo_pontos.configure(text=f"{acertos}/{total}")
        self.rotulo_comentario.configure(text=_comentario(acertos, total))

    def _montar_menu(self) -> None:
        self.quadro_menu = tk.Frame(self.conteudo, bg=CORES["fundo"])
        miolo = tk.Frame(self.quadro_menu, bg=CORES["fundo"])
        miolo.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            miolo,
            text="Questões de Português",
            font=self.fonte_titulo,
            bg=CORES["fundo"],
            fg=CORES["tinta"],
        ).pack(anchor="w")
        tk.Label(
            miolo,
            text="Treino de crase, de hífen e de análise sintática com frases de prova.\nDez questões por rodada, sem repetir.",
            font=self.fonte_ui,
            bg=CORES["fundo"],
            fg=CORES["mudo"],
            justify="left",
        ).pack(anchor="w", pady=(8, 28))

        botoes = tk.Frame(miolo, bg=CORES["fundo"])
        botoes.pack(fill="x")
        self._botao_tema(botoes, "Crase", "crase").pack(fill="x", pady=(0, 10))
        self._botao_tema(botoes, "Hífen", "hifen").pack(fill="x", pady=(0, 10))
        self._botao_tema(botoes, "Análise sintática", "sintaxe").pack(fill="x")

        tk.Label(
            miolo,
            text="Escolha um tema. Em cada frase, o trecho em destaque está certo ou errado.",
            font=self.fonte_miuda,
            bg=CORES["fundo"],
            fg=CORES["mudo"],
        ).pack(anchor="w", pady=(24, 0))

    def _botao_tema(self, pai: tk.Widget, texto: str, tema: str) -> tk.Button:
        return tk.Button(
            pai,
            text=texto,
            font=self.fonte_botao,
            bg=CORES["azul"],
            fg=CORES["branco"],
            activebackground=CORES["azul_ativo"],
            activeforeground=CORES["branco"],
            relief="flat",
            cursor="hand2",
            width=22,
            height=2,
            command=lambda: self.iniciar(tema),
        )

    def _montar_questao(self) -> None:
        self.quadro_questao = tk.Frame(self.conteudo, bg=CORES["fundo"], padx=28, pady=22)
        self._ajustando_rolagem = False

        self.rodape_questao = tk.Frame(self.quadro_questao, bg=CORES["fundo"])
        self.rodape_questao.pack(side="bottom", fill="x", pady=(12, 0))

        topo = tk.Frame(self.quadro_questao, bg=CORES["fundo"])
        topo.pack(fill="x")
        self.rotulo_progresso = tk.Label(
            topo, text="", font=self.fonte_ui_bold, bg=CORES["fundo"], fg=CORES["azul"]
        )
        self.rotulo_progresso.pack(side="left")
        tk.Button(
            topo,
            text="Menu",
            font=self.fonte_miuda,
            bg=CORES["fundo"],
            fg=CORES["mudo"],
            relief="flat",
            cursor="hand2",
            command=self.mostrar_menu,
        ).pack(side="right")

        cartao = tk.Frame(
            self.quadro_questao,
            bg=CORES["cartao"],
            highlightbackground=CORES["contorno"],
            highlightthickness=1,
            padx=22,
            pady=18,
        )
        cartao.pack(fill="x", pady=(18, 0))
        self.texto_frase = tk.Text(
            cartao,
            font=self.fonte_frase,
            bg=CORES["cartao"],
            fg=CORES["tinta"],
            wrap="word",
            height=3,
            relief="flat",
            highlightthickness=0,
            cursor="arrow",
        )
        self.texto_frase.tag_configure(
            "destaque",
            background=CORES["destaque"],
            font=_primeira_fonte(self.raiz, ("Georgia", "Liberation Serif", "DejaVu Serif"), 20, "bold"),
        )
        self.texto_frase.pack(fill="x")
        self.texto_frase.configure(state="disabled")

        self.rotulo_pergunta = tk.Label(
            self.quadro_questao,
            text="O trecho em destaque está de acordo com a norma?",
            font=self.fonte_ui,
            bg=CORES["fundo"],
            fg=CORES["mudo"],
        )
        self.rotulo_pergunta.pack(anchor="w", pady=(16, 8))

        acoes = tk.Frame(self.quadro_questao, bg=CORES["fundo"])
        acoes.pack(fill="x")
        self.botao_certo = self._botao_acao(acoes, "Certo", True, CORES["azul"])
        self.botao_certo.pack(side="left", padx=(0, 10))
        self.botao_errado = self._botao_acao(acoes, "Errado", False, "#7f1d1d")
        self.botao_errado.pack(side="left")

        self.faixa_feedback = tk.Frame(self.quadro_questao, bg=CORES["fundo"])
        self.canvas_feedback = tk.Canvas(
            self.faixa_feedback,
            bg=CORES["fundo"],
            highlightthickness=0,
            borderwidth=0,
        )
        self.scroll_feedback = tk.Scrollbar(
            self.faixa_feedback,
            orient="vertical",
            command=self.canvas_feedback.yview,
        )
        self.canvas_feedback.configure(yscrollcommand=self._rolagem_ajustada)
        self.canvas_feedback.pack(side="left", fill="both", expand=True)
        self.painel_feedback = tk.Frame(
            self.canvas_feedback,
            bg=CORES["acerto_fundo"],
            padx=16,
            pady=14,
        )
        self.janela_feedback = self.canvas_feedback.create_window(
            (0, 0), window=self.painel_feedback, anchor="nw"
        )
        self.painel_feedback.bind("<Configure>", self._sincronizar_rolagem)
        self.canvas_feedback.bind("<Configure>", self._sincronizar_rolagem)
        for alvo in (self.faixa_feedback, self.canvas_feedback, self.painel_feedback):
            alvo.bind("<Enter>", self._ativar_rolagem)
            alvo.bind("<Leave>", self._desativar_rolagem)
        self.rotulo_feedback = tk.Label(
            self.painel_feedback,
            text="",
            font=self.fonte_ui_bold,
            bg=CORES["acerto_fundo"],
            fg=CORES["acerto_tinta"],
            anchor="w",
        )
        self.rotulo_feedback.pack(fill="x")
        self.rotulo_julgamento = tk.Label(
            self.painel_feedback,
            text="",
            font=self.fonte_ui,
            bg=CORES["acerto_fundo"],
            fg=CORES["tinta"],
            anchor="w",
        )
        self.rotulo_julgamento.pack(fill="x", pady=(2, 8))
        self.rotulo_explicacao = tk.Label(
            self.painel_feedback,
            text="",
            font=self.fonte_ui,
            bg=CORES["cartao"],
            fg=CORES["tinta"],
            anchor="w",
            justify="left",
            wraplength=760,
            padx=12,
            pady=10,
        )
        self.rotulo_explicacao.pack(fill="x")
        self.rotulo_regra = tk.Label(
            self.painel_feedback,
            text="",
            font=self.fonte_ui_bold,
            bg=CORES["cartao"],
            fg=CORES["azul"],
            anchor="w",
            justify="left",
            wraplength=760,
            padx=12,
            pady=4,
        )
        self.rotulo_regra.pack(fill="x")
        self.rotulo_fonte = tk.Label(
            self.painel_feedback,
            text="",
            font=self.fonte_miuda,
            bg=CORES["cartao"],
            fg=CORES["mudo"],
            anchor="w",
            justify="left",
            wraplength=760,
            padx=12,
            pady=8,
        )
        self.rotulo_fonte.pack(fill="x", pady=(0, 8))

        self.botao_proxima = tk.Button(
            self.rodape_questao,
            text="Próxima",
            font=self.fonte_botao,
            bg=CORES["azul"],
            fg=CORES["branco"],
            activebackground=CORES["azul_ativo"],
            activeforeground=CORES["branco"],
            disabledforeground=CORES["mudo"],
            relief="flat",
            cursor="hand2",
            width=16,
            height=2,
            state="disabled",
            command=self.proxima,
        )
        self.botao_proxima.pack(side="right")
        self._estado_proxima(False, "Próxima")

    def _estado_proxima(self, habilitado: bool, texto: str) -> None:
        if habilitado:
            self.botao_proxima.configure(
                state="normal",
                text=texto,
                bg=CORES["azul"],
                fg=CORES["branco"],
            )
        else:
            self.botao_proxima.configure(
                state="disabled",
                text=texto,
                bg="#e7dfd4",
                fg=CORES["mudo"],
            )

    def _ativar_rolagem(self, _evento: tk.Event) -> None:
        self.canvas_feedback.bind_all("<Button-4>", self._rolar)
        self.canvas_feedback.bind_all("<Button-5>", self._rolar)
        self.canvas_feedback.bind_all("<MouseWheel>", self._rolar)

    def _desativar_rolagem(self, _evento: tk.Event) -> None:
        self.canvas_feedback.unbind_all("<Button-4>")
        self.canvas_feedback.unbind_all("<Button-5>")
        self.canvas_feedback.unbind_all("<MouseWheel>")

    def _rolar(self, evento: tk.Event) -> None:
        if getattr(evento, "num", None) == 4:
            self.canvas_feedback.yview_scroll(-3, "units")
        elif getattr(evento, "num", None) == 5:
            self.canvas_feedback.yview_scroll(3, "units")
        else:
            self.canvas_feedback.yview_scroll(int(-evento.delta / 120), "units")

    def _rolagem_ajustada(self, primeiro: str, ultimo: str) -> None:
        self.scroll_feedback.set(primeiro, ultimo)
        if float(primeiro) <= 0 and float(ultimo) >= 1:
            self.scroll_feedback.pack_forget()
        elif not self.scroll_feedback.winfo_manager():
            self.scroll_feedback.pack(side="right", fill="y")

    def _sincronizar_rolagem(self, _evento: tk.Event | None = None) -> None:
        if self._ajustando_rolagem:
            return
        self._ajustando_rolagem = True
        try:
            self.canvas_feedback.update_idletasks()
            largura = self.canvas_feedback.winfo_width()
            if largura > 1:
                self.canvas_feedback.itemconfigure(self.janela_feedback, width=largura)
                for rotulo in (self.rotulo_explicacao, self.rotulo_regra, self.rotulo_fonte):
                    rotulo.configure(wraplength=max(280, largura - 56))
            caixa = self.canvas_feedback.bbox("all")
            if caixa is not None:
                self.canvas_feedback.configure(scrollregion=caixa)
        finally:
            self._ajustando_rolagem = False

    def _botao_acao(self, pai: tk.Widget, texto: str, valor: bool, cor: str) -> tk.Button:
        return tk.Button(
            pai,
            text=texto,
            font=self.fonte_botao,
            bg=cor,
            fg=CORES["branco"],
            activebackground=cor,
            activeforeground=CORES["branco"],
            relief="flat",
            cursor="hand2",
            width=14,
            height=2,
            command=lambda: self.responder(valor),
        )

    def _montar_resultado(self) -> None:
        self.quadro_resultado = tk.Frame(self.conteudo, bg=CORES["fundo"])
        miolo = tk.Frame(self.quadro_resultado, bg=CORES["fundo"])
        miolo.place(relx=0.5, rely=0.5, anchor="center")
        self.rotulo_tema_final = tk.Label(
            miolo, text="", font=self.fonte_ui_bold, bg=CORES["fundo"], fg=CORES["azul"]
        )
        self.rotulo_tema_final.pack()
        tk.Label(
            miolo, text="Pontuação", font=self.fonte_ui, bg=CORES["fundo"], fg=CORES["mudo"]
        ).pack(pady=(8, 0))
        self.rotulo_pontos = tk.Label(
            miolo, text="", font=self.fonte_pontos, bg=CORES["fundo"], fg=CORES["tinta"]
        )
        self.rotulo_pontos.pack()
        self.rotulo_comentario = tk.Label(
            miolo,
            text="",
            font=self.fonte_ui,
            bg=CORES["fundo"],
            fg=CORES["mudo"],
            wraplength=460,
            justify="center",
        )
        self.rotulo_comentario.pack(pady=(4, 24))
        linha = tk.Frame(miolo, bg=CORES["fundo"])
        linha.pack()
        tk.Button(
            linha,
            text="Jogar de novo",
            font=self.fonte_botao,
            bg=CORES["azul"],
            fg=CORES["branco"],
            activebackground=CORES["azul_ativo"],
            activeforeground=CORES["branco"],
            relief="flat",
            cursor="hand2",
            width=16,
            height=2,
            command=self._jogar_de_novo,
        ).pack(side="left", padx=(0, 10))
        tk.Button(
            linha,
            text="Voltar ao menu",
            font=self.fonte_botao,
            bg=CORES["cartao"],
            fg=CORES["azul"],
            relief="flat",
            cursor="hand2",
            width=16,
            height=2,
            highlightbackground=CORES["contorno"],
            command=self.mostrar_menu,
        ).pack(side="left")

    def _jogar_de_novo(self) -> None:
        if self.tema is None:
            self.mostrar_menu()
            return
        self.iniciar(self.tema)

    def _atalho_resposta(self, valor: bool) -> None:
        if self.sessao is not None and not self.sessao.respondida and self.quadro_questao.winfo_ismapped():
            self.responder(valor)

    def _atalho_avancar(self) -> None:
        if (
            self.sessao is not None
            and self.sessao.respondida
            and self.quadro_questao.winfo_ismapped()
        ):
            self.proxima()


def _comentario(acertos: int, total: int) -> str:
    if acertos == total:
        return "Dez em dez. A rodada fechou sem erro."
    if acertos >= 7:
        return "Bom resultado. Dá para firmar o que ainda oscilou jogando de novo."
    if acertos >= 5:
        return "Metade ou um pouco mais. Vale repetir o tema com outras frases."
    return "A rodada mostrou o que revisar. A explicação de cada item continua no banco."


def main() -> None:
    raiz = tk.Tk()
    try:
        Aplicativo(raiz)
    except (OSError, ValueError, KeyError) as erro:
        messagebox.showerror("Questões de Português", f"Não foi possível abrir o banco.\n{erro}")
        raiz.destroy()
        return
    raiz.mainloop()
