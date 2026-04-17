from cinema.services import utils
from cinema.UI.CLI import menu_filmes, menu_salas
import questionary

def menu_adm():
    print("Acessando serviços de Administrador...")

    choices = [
        questionary.Choice("Gerenciar filmes", value=1),
        questionary.Choice("Gerenciar salas", value=2),
        questionary.Choice("Sair", value=0)
    ]

    opcao = questionary.select(
        "Escolha:",
        choices=choices
    ).ask()


    if opcao == 1:
        menu_filmes.menu_filmes()
    elif opcao == 2:
        menu_salas.menu_salas()
    elif opcao == 0:
        print("Voltando para o inicio...")
        print("\n" + "-" * 40 + "\n")
