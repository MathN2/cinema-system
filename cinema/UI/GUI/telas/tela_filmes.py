import tkinter as tk
from cinema.data import loading_db

def abrir_tela_filmes(root):
    janela = tk.Frame(root)
    root.pack_forget()
    janela.pack()

    titulo = tk.Label(janela, text="Lista de Filmes", font=("Arial", 14))
    titulo.pack(pady=10)

    lista_frame = tk.Frame(janela)
    lista_frame.pack(fill="both", expand=True)

    filmes = loading_db.load_movies()

    if not filmes:
        tk.Label(lista_frame, text="Nenhum filme encontrado.").pack()
        return
    
    for filme in filmes:
        texto = f"{filme['titulo']}"
        tk.Label(lista_frame, text=texto).pack(anchor="w", padx=10)