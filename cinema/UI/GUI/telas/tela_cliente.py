import tkinter as tk
from cinema.data.loading_db import load_movies
from cinema.models.filme import Movie
from cinema.models.sessao import Section
from cinema.services import sessao_services
from cinema.data.saving_db import update_section_assentos


# ================================================================
#                       APP PRINCIPAL
# ================================================================
def open_client():
    global tela_atual, selecionados

    root = tk.Tk()
    root.title("Cinema")
    root.geometry("900x600")  # 🔽 ADICIONADO: tamanho fixo

    # 🔽 ADICIONADO: estilo base do app
    root.configure(bg="#1e1e1e")

    header = tk.Label(
        root,
        text="🎬 Bem-vindo ao Cinema",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e1e1e"
    )
    header.pack(pady=15)

    tela_atual = None
    selecionados = set()

    tela_filmes(root)

    root.mainloop()


# ================================================================
#                       TROCA DE TELAS
# ================================================================
def trocar_tela(nova_tela):
    global tela_atual

    if tela_atual is not None:
        tela_atual.destroy()

    tela_atual = nova_tela
    tela_atual.pack(expand=True, fill="both", padx=20, pady=10)  # 🔽 MELHORADO


# ================================================================
#                       FILMES
# ================================================================
def tela_filmes(root):

    lista_filmes = load_movies()

    frame = tk.Frame(root, bg="#2b2b2b")
    trocar_tela(frame)

    titulo = tk.Label(
        frame,
        text="Filmes disponíveis",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#2b2b2b"
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=15)

    if not lista_filmes:
        tk.Label(
            frame,
            text="Nenhum filme disponível",
            fg="white",
            bg="#2b2b2b"
        ).grid(row=1)

    for i, filme in enumerate(lista_filmes):
        tk.Label(
            frame,
            text=filme['titulo'],
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 11)
        ).grid(row=i+1, column=0, sticky="w", padx=20, pady=5)

        tk.Button(
            frame,
            text="Assistir",
            bg="#2196F3",
            fg="white",
            width=10,
            command=lambda filme=filme: escolha_dia(root, filme)
        ).grid(row=i+1, column=1, padx=10, pady=5)


# ================================================================
#                       DIAS
# ================================================================
def escolha_dia(root, filme):

    filme = Movie(**filme)
    datas = sessao_services.get_section_by_date_hour(filme)

    frame = tk.Frame(root, bg="#2b2b2b")
    trocar_tela(frame)

    tk.Label(
        frame,
        text="Escolha o dia",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#2b2b2b"
    ).pack(pady=10)

    grid = tk.Frame(frame, bg="#2b2b2b")
    grid.pack()

    for i, item in enumerate(datas):
        tk.Button(
            grid,
            text=item['label'],
            width=18,
            bg="#555",
            fg="white",
            command=lambda item=item: escolha_horario(root, item, filme)
        ).grid(row=i//4, column=i%4, padx=8, pady=8)


# ================================================================
#                       HORÁRIOS
# ================================================================
def escolha_horario(root, item, filme):

    frame = tk.Frame(root, bg="#2b2b2b")
    trocar_tela(frame)

    tk.Label(
        frame,
        text="Escolha o horário",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#2b2b2b"
    ).pack(pady=10)

    grid = tk.Frame(frame, bg="#2b2b2b")
    grid.pack()

    for i, horario in enumerate(item['horarios']):
        tk.Button(
            grid,
            text=str(horario),
            width=10,
            bg="#444",
            fg="white",
            command=lambda item=item, horario=horario: definir_sessao(item['data'], horario, filme)
        ).grid(row=i//5, column=i%5, padx=5, pady=5)


# ================================================================
#                       ASSENTOS
# ================================================================
def definir_sessao(data, horario, filme):
    global selecionados
    selecionados.clear()

    data_hora = f'{data}_{horario}'
    dados_sessao = sessao_services.get_section(filme, data_hora)

    sessao_obj = Section.from_dict(dados_sessao)

    renderizar_assentos(tela_atual, sessao_obj)


def renderizar_assentos(frame, sessao_obj):

    for widget in frame.winfo_children():
        widget.destroy()

    # ================================================================
    # CONTAINER PRINCIPAL (divide esquerda e direita)
    # ================================================================
    container = tk.Frame(frame, bg="#1e1e1e")
    container.pack(fill="both", expand=True)

    # ================================================================
    # LADO ESQUERDO -> ASSENTOS
    # ================================================================
    left = tk.Frame(container, bg="#1e1e1e")
    left.pack(side="left", expand=True, fill="both")

    # “tela do cinema”
    tk.Label(
        left,
        text="TELA",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=10)

    grid = tk.Frame(left, bg="#1e1e1e")
    grid.pack()

    for linha_nome, linha in sessao_obj.assentos.items():

        tk.Label(
            grid,
            text=linha_nome,
            fg="white",
            bg="#1e1e1e"
        ).grid(row=ord(linha_nome)-65, column=0, padx=5)

        for i, assento in enumerate(linha):

            lugar = f"{linha_nome}{i+1}"

            if assento == '[X]':
                cor = "#F44336"
                fg = "white"
                estado = "disabled"

            elif lugar in selecionados:
                cor = "#FFC107"
                fg = "black"
                estado = "normal"

            else:
                cor = "#4CAF50"
                fg = "white"
                estado = "normal"

            tk.Button(
                grid,
                text=lugar,
                bg=cor,
                fg=fg,
                disabledforeground=fg,
                width=4,
                height=2,
                state=estado,
                command=lambda l=lugar: clicar_assento(l, sessao_obj, frame)
            ).grid(row=ord(linha_nome)-65, column=i+1, padx=2, pady=2)

    # ================================================================
    # LADO DIREITO -> PAINEL
    # ================================================================
    right = tk.Frame(container, bg="#1e1e1e", width=200)
    right.pack(side="right", fill="y")

    # fixa largura do painel
    right.pack_propagate(False)

    # ------------------------------------------------
    # LEGENDA
    # ------------------------------------------------
    tk.Label(
        right,
        text="Legenda",
        fg="white",
        bg="#1e1e1e",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Label(right, text="Disponível", bg="#4CAF50", fg="white", width=15).pack(pady=3)
    tk.Label(right, text="Ocupado", bg="#F44336", fg="white", width=15).pack(pady=3)
    tk.Label(right, text="Selecionado", bg="#FFC107", fg="black", width=15).pack(pady=3)

    # ------------------------------------------------
    # BOTÃO CONFIRMAR
    # ------------------------------------------------
    tk.Button(
        right,
        text="Confirmar seleção",
        bg="#2196F3",
        fg="white",
        width=18,
        command=lambda: confirmar_compra(sessao_obj, frame)
    ).pack(pady=20)


# ================================================================
#                       LÓGICA
# ================================================================
def clicar_assento(lugar, sessao_obj, frame):
    global selecionados

    if lugar in selecionados:
        selecionados.remove(lugar)
    else:
        selecionados.add(lugar)

    atualizar_tela(frame, sessao_obj)


def confirmar_compra(sessao_obj, frame):
    global selecionados

    for lugar in selecionados:
        sessao_obj.assign_seat(lugar)

    update_section_assentos(sessao_obj)

    selecionados.clear()

    voltar_menu(frame)


def voltar_menu(frame):
    root = frame.master
    tela_filmes(root)


def atualizar_tela(frame, sessao_obj):
    renderizar_assentos(frame, sessao_obj)