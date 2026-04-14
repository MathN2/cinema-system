from cinema.services import utils
from cinema.UI.CLI import menu_filmes, menu_salas

def menu_adm():
    print("Acessando serviços de Administrador...")

    mensagem = '''
1 - Gerenciar Filmes
2 - Gerenciar Salas
0 - Sair
'''
    
    opcao = utils.validar_int(0, 2, mensagem)

    if opcao == 1:
        menu_filmes.menu_filmes()
    elif opcao == 2:
        menu_salas.menu_salas()
    elif opcao == 0:
        print("Voltando para o inicio...")
        print("\n" + "-" * 40 + "\n")
