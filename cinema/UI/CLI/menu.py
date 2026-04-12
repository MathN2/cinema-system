# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#     Interface no terminal para interacao direta com o usuario (Administrador ou Cliente).


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#     Definir valores de ingresso (inteira e meia) []
#     Exibir resumo da compra (assento, filme, horário, valor) []
#     Calcular valor total da compra []
#     Login de ADM e login de cliente []
#     Interface de texto (inicial) []
#     (Futuramente) Adicionar interface gráfica []


from cinema.UI.CLI.menu_adm import menu_adm
from cinema.UI.CLI.menu_cliente import menu_client

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
        print('LOGN IN')
        #Melhorar
        adm = input('1 - ADMINISTRADOR\n2 - CLIENTE\n')
        adm = True if adm == '1' else False

        if adm == True:
            menu_adm()
            
        else:
            menu_client()
