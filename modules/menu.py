# MENU PARA INTERAÇÃO DO USUARIO

#  Definir valores de ingresso (inteira e meia) []
#  Exibir resumo da compra (assento, filme, horário, valor) []
#  Calcular valor total da compra []
#  Login de ADM e login de cliente []
#  Interface de texto (inicial) []
#  (Futuramente) Adicionar interface gráfica []

import models
import storage
from time import sleep


def menu_adm():
    print("Acessando serviços de Administrador...")
    sleep(1)

    print("""
            1 - Exibir filmes cadastrados.
            2 - Cadastrar novo filme.
            3 - Remover filme.
            4 - Modificar configuração de filme.
            5 - Sair.
            """)


def menu_client():
    print('*' * 50)
    print('BEM-VINDO'.center(50, ' '))
    print('*' * 50)

    print("Filmes em cartaz:")
    

def Menu():
    print("Iniciando Sistema Cinema")

    print('LOGN IN')
    adm = input('1 - ADMINISTRADOR\n2 - CLIENTE\n')
    adm = True if adm == '1' else False

    if adm == True:
        menu_adm()
        
    else:
        menu_client()
Menu()