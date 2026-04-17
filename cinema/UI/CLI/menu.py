from cinema.UI.CLI.menu_adm import menu_adm
from cinema.UI.CLI.menu_cliente import menu_client
import questionary

# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#     Interface no terminal para interacao direta com o usuario (Administrador ou Cliente).


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#     Definir valores de ingresso (inteira e meia) []
#     Exibir resumo da compra (assento, filme, horário, valor) []
#     Calcular valor total da compra []
#     Login de ADM e login de cliente []
#     Interface de texto (inicial) []
#     (Futuramente) Adicionar interface gráfica []



# ================================================================
#                       MENU PRINCIPAL
# ================================================================
def menu_principal():
    """
    Mostra o menu principal, permitindo o usuario escolher o tipo de Login fazer (Administrador ou Cliente).

    *EM PROGRESSO*
    """
    print("Iniciando Sistema Cinema")
    while True:
        print('LOGIN')

        choices = [
            questionary.Choice("Administrador", value="adm"),
            questionary.Choice("Cliente", value="cli"),
            questionary.Choice("Sair", value="exit")
        ]

        escolha = questionary.select(
            "Como deseja entrar?",
            choices= choices
        ).ask()

        if escolha == "adm":
            menu_adm()
        elif escolha == "cli":
            menu_client()
        else:
            break
