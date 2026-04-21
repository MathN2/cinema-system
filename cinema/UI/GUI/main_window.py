import tkinter as tk
from cinema.UI.GUI.telas.tela_filmes import abrir_tela_filmes

def main():
    root = tk.Tk()
    root.title("Cinema Manager")
    root.geometry("400x300")

    titulo = tk.Label(root, text="Sistema Cinema", font=("Arial", 16))
    titulo.pack(pady=20)

    btn_filmes = tk.Button(
        root,
        text="Filmes",
        width=20,
        command=lambda: abrir_tela_filmes(root)
    )
    btn_filmes.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()